from collections import defaultdict

from django.shortcuts import render

# Create your views here.
import json
import re
from datetime import datetime
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from common import models
from common.models import Admin
# Create your views here.
from django.views import View
from common.models import Admin, Position, Right, Menu
from utils import functions
from utils.common_mixin import AdminLoggedMixin, AdminMixin
from django.utils.encoding import smart_str
from django.utils.encoding import smart_text


class AdminLoginView(View):
    def __init__(self):
        super().__init__()
        self.context = {}
        self.admin_info = {}

    def get(self, request):
        return render(request, 'admin/login.html', self.context)

    def post(self, request):
        email_or_username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        self.context['code'] = 200
        if not email_or_username:
            self.context['code'] = 400
            self.context['msg'] = '请输入用户名'
        elif not password:
            self.context['code'] = 400
            self.context['msg'] = '请输入密码'
        else:
            check = Admin.objects.filter(Q(email=email_or_username) | Q(name=email_or_username) & Q(is_deleted=0))
            if check:
                admin_obj = check.first()
                secret_password = functions.my_md5(flag=1, password=password)
                if admin_obj.password == secret_password:
                    if 'HTTP_X_FORWARDED_FOR' in request.META:
                        ip = request.META['HTTP_X_FORWARDED_FOR']
                    else:
                        ip = request.META['REMOTE_ADDR']
                    self.admin_info['admin_name'] = admin_obj.name
                    self.admin_info['admin_id'] = admin_obj.id
                    self.admin_info["is_sysop"] = admin_obj.is_sysop
                    self.admin_info['ip'] = ip
                    request.session['admin_info'] = self.admin_info
                    admin_obj.log_times += 1
                    admin_obj.last_log_ip = ip
                    admin_obj.last_log_time = datetime.now()
                    admin_obj.save()
                    self.context['msg'] = '登录成功'
                    response = HttpResponse(json.dumps(self.context))
                    name2 = json.dumps(admin_obj.name)
                    response.set_cookie('admin_name', name2)
                    return response
                else:
                    self.context['code'] = 400
                    self.context['msg'] = '登录密码错误'
            else:
                self.context['code'] = 400
                self.context['msg'] = '用户不存在'
        return HttpResponse(json.dumps(self.context))


class AdminView(AdminLoggedMixin, View):
    def get_template(self, request):
        if self.if_list:
            self.template = "admin/list.html"
        else:
            rights = Right.objects.all().values("id", "action_group_id", "action_group__group", "action")
            res = defaultdict(list)
            for right in rights:
                res[right['action_group_id']].append((right['id'], right['action_group__group'], right['action']))
            self.context.update({"rights": dict(res)})

            own_rights = Admin.objects.get(id=self.obj_id).rights.all().values_list("id", flat=True)
            self.context.update({"own_rights": own_rights})

            all_position = Position.objects.filter(is_deleted=0).values("id", "name")
            self.context.update({"all_position": all_position})
            self.template = "admin/detail.html"

    def get_list_values(self):
        self.list_values = [
            "id",
            "name",
            "add_time",
            "last_log_ip",
            ["position__name", "pos"],
            "last_log_time",
            "log_times"
        ]

    def get_detail_values(self):
        self.detail_values = [
            "id",
            "name",
            ["position.id", "position_id"],
            ["position.name", "position_name"],
        ]

    # "status",
    # 当前model的字段，关联的model, 类型， 反向关联的字段
    # ["content", "Content", "foreign_key", "article_id"],
    # ["tags", "Tag", "many2many"]
    def get_post_data(self):
        self.post_data = [
            "name",
            "password",
            "position_id",
            ["rights", "Right", "many2many"],
        ]
        self.not_same = True

    def get_put_data(self):
        self.put_data = [
            "name",
            "password",
            "position_id",
            ["rights", "Right", "many2many"],
        ]

    def get(self, request):
        self.model = Admin
        self.get_list_values()
        self.get_detail_values()
        self.get_template(request)
        self.and_field = {"is_deleted": 0, "is_sysop": 0}
        return super().get(request)

    def post(self, request):
        self.model = Admin
        self.is_ajax = 1
        self.get_post_data()
        return super().post(request)

    def put(self, request):
        self.model = Admin
        # 与post一样
        self.is_ajax = 1
        self.get_put_data()
        return super().put(request)

    def delete(self, request):
        self.model = Admin
        self.is_ajax = 1
        return super().delete(request)


class AdminAdd(AdminLoggedMixin, View):
    def __init__(self):
        super().__init__()

    def get(self, request):
        rights = Right.objects.all().values("id", "action_group_id", "action_group__group", "action")
        res = defaultdict(list)
        for right in rights:
            res[right['action_group_id']].append((right['id'], right['action_group__group'], right['action']))
        self.context.update({"rights": dict(res)})

        self.model = Position
        self.list_values = [
            "id",
            "name"
        ]
        self.and_field = {"is_deleted": 0}
        self.template = "admin/add.html"
        return super().get(request)


class MainView(AdminMixin, View):
    def get(self, request):
        if "outer" in self.url:
            self.context["data"] = {}
            self.context["data"].update({"quick": Menu.objects.filter(
                admin_id=self.admin_id).order_by("-click_time").values("url", "name")[:4]})
            self.template = "public/outer_2.html"
        else:
            self.template = "public/main.html"
        return super().get(request)


class LogoutView(View):
    def get(self, request):
        del request.session["admin_info"]
        return HttpResponseRedirect("/admin/login/")
