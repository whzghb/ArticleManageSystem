import json
import re
from datetime import datetime
from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from ArticleManageSystem import settings
from ArticleManageSystem.settings import DATETIME_FORMAT
from django.db.models import F
from common.models import Article, Content, Admin, Right, Menu, FeedBack, Comment
from django.http import QueryDict
from utils import functions
from utils.signal import log


class AdminMixin(object):
    def __init__(self):
        self.ip = None
        self.template = ''
        self.admin_info = {}
        self.context = {}
        self.is_ajax = 0
        self.error = {}
        self.count = None
        self.url = "/article/draft/"
        self.if_has_right = False
        self.method = None
        self.admin_id = None
        self.is_sysop = False
        self.if_list = True
        self.cur_page = 1

    # 确定以何种方式返回数据
    def check_method(self, request):
        if self.error:
            return render(request, self.template, self.error)
        self.context.update({"admin": request.session.get("admin_info").get("admin_name")})
        if self.is_ajax == 0:
            return render(request, self.template, self.context)
        else:
            return HttpResponse(json.dumps(self.context))

    def pre_get(self, request):
        pass

    def get(self, request):
        self.pre_get(request)
        rlt = self.check_method(request)
        return rlt

    def pre_post(self, request):
        pass

    def post(self, request):
        self.pre_post(request)
        rlt = self.check_method(request)
        return rlt

    def pre_delete(self, request):
        pass

    def delete(self, request):
        self.pre_delete(request)
        rlt = self.check_method(request)
        return rlt

    def pre_put(self, request):
        pass

    def put(self, request):
        self.pre_delete(request)
        rlt = self.check_method(request)
        return rlt

    # 判断是否登录
    def initialize(self, request):
        try:
            self.admin_info = request.session['admin_info']
        except Exception:
            self.template = 'admin/login.html'

    # 获取管理员id和判断是否超级管理员
    def get_admin_id(self):
        self.admin_id = self.admin_info.get("admin_id", 1)
        self.is_sysop = self.admin_info.get("is_sysop", True)

    # 判断是否有权限
    def get_right(self, request):
        self.url = request.path
        self.method = request.method
        self.get_admin_id()
        if (self.url, self.method) in settings.WHITE_URL:
            self.if_has_right = True
        elif self.is_sysop:
            self.if_has_right = True
        else:
            right_id = Right.objects.get(url=self.url, type=self.method).id
            self.if_has_right = Admin.objects.get(id=self.admin_id).rights.filter(admin__rights=right_id)

    # 判断列表还是详情
    def check_if_list(self, request):
        if_list = request.GET.get("id", "")
        if if_list:
            self.if_list = False
            self.obj_id = int(if_list)
        else:
            self.if_list = True

    def menu_click(self):
        if self.url in [url for url in settings.MENU_URL]:
            try:
                obj = Menu.objects.get(url=self.url, admin_id=self.admin_id)
                obj.click_time += 1
                obj.save()
            except Exception:
                Menu.objects.create(url=self.url, name=settings.MENU_URL[self.url], admin_id=self.admin_id)

    def dispatch(self, request, *args, **kwargs):
        # TODO
        self.initialize(request)
        if self.template:
            return HttpResponseRedirect("/admin/login/")
        self.get_right(request)
        if not self.if_has_right:
            if self.method == "GET":
                return render(request, "public/forbiden.html")
            else:
                return HttpResponse(json.dumps({"code": "403", "msg": "权限不足"}))
        self.check_if_list(request)
        self.menu_click()
        return super().dispatch(request, *args, **kwargs)


class AdminLoggedMixin(AdminMixin):
    def __init__(self):
        super().__init__()
        # 使用的数据表
        self.model = None
        # 当前对象id
        self.obj_id = None
        # {filed: condition}
        self.or_field = {}
        self.and_field = {}
        # 列表展示的字段
        self.list_values = []
        # 详情展示的字段
        self.detail_values = []
        # 分页后的查询结果集
        self.page_query_set = None
        # 当前对象
        self.obj = None
        # 要搜索的字段
        self.search_field = None
        # post请求时发送的字段
        self.post_data = []
        # put请求时发送的字段
        self.put_data = []
        # 展示详情时获取哪个字段以获取信息
        self.detail_id_field = "id"
        # 是否需要分页
        self.need_page = True
        self.not_same = False

    def get_template(self, request):
        pass

    def get_model(self, request):
        pass

    def get_extra_fields(self, request):
        pass

    def get_list_values(self):
        pass

    def get_detail_values(self):
        pass

    def get_filter(self, request, query_set):
        search = request.GET.get('search', '')
        rlt_and_field = []
        rlt_or_field = []
        if search:
            for field in self.search_field:
                rlt_or_field.append('Q(%s__icontains="%s")' % (field, search))
        for field, condition in self.or_field.items():
            if isinstance(condition, int):
                rlt_or_field.append('Q(%s=%s)' % (field, condition))
            else:
                rlt_or_field.append('Q(%s="%s")' % (field, condition))
        for field, condition in self.and_field.items():
            if isinstance(condition, int):
                rlt_and_field.append('Q(%s=%s)' % (field, condition))
            else:
                rlt_and_field.append('Q(%s="%s")' % (field, condition))
        if rlt_or_field:
            str_or_filter = '(' + ' | '.join(rlt_or_field) + ')' + ' & '
        else:
            str_or_filter = ""
        str_and_filter = ' & '.join(rlt_and_field)
        if not str_and_filter:
            str_or_filter = str_or_filter[:-3]
        condition = str_or_filter + str_and_filter
        if condition:
            query_set = query_set.filter(eval(condition))
        return query_set

    # 分页，搜索，排序，过滤
    def get_page(self, request, query_set):
        page = request.GET.get('page', '')
        size = request.GET.get('size', '')
        if not page:
            page = 1
        if not size:
            size = 10
        page = int(page)
        size = int(size)
        self.count = query_set.count()
        self.page = page
        if self.count:
            page_num = self.count // size if self.count % size == 0 else self.count//size+1
            if page_num <= 9:
                show_page = {"show_page": [i+1 for i in range(page_num)]}
            elif self.page < 5:
                show_page = {"show_page": [i+1 for i in range(9)]}
            elif page_num - self.page < 5:
                show_page = {"show_page": [i+1 for i in range(page_num)[-9:]]}
            else:
                show_page = {"show_page": [i for i in range(self.page-4, self.page+5)]}
            self.context.update(show_page)
            self.context.update({"cur_page": self.page})
            self.context.update({"count": self.count})
            self.context.update({"page_num": page_num})
        else:
            self.context.update({"count": 0})
        self.page_query_set = query_set[(self.page - 1) * size:(self.page - 1) * size + size]

    # "reject_reason",
    # ["adder__name", "adder_name"],
    # "content",
    # ["article.tags.all().values('name', 'id')", "tags"],
    # 重命名
    # 封装get
    def get(self, request):
        self.obj_id = request.GET.get('id', '')
        if not self.obj_id:
            query_set = self.model.objects.all()
            query_set = self.get_filter(request, query_set)
            all_field_dict = {}
            all_field_list = []
            for field in self.list_values:
                if isinstance(field, str):
                    all_field_list.append(field)
                else:
                    all_field_dict[field[1]] = F(field[0])
            if self.need_page:
                self.get_page(request, query_set)
                if self.list_values:
                    self.context["data"] = self.page_query_set.values(*all_field_list, **all_field_dict)
                else:
                    self.context["data"] = self.page_query_set
            else:
                if self.list_values:
                    self.context["data"] = query_set.values(*all_field_list, **all_field_dict)
                else:
                    self.context["data"] = query_set
        else:
            self.obj_id = int(self.obj_id)
            filter_dict = {self.detail_id_field: self.obj_id}
            check = self.model.objects.filter(**filter_dict)
            if check:
                self.obj = check.first()
                rlt = {}
                if self.detail_values:
                    for field in self.detail_values:
                        if isinstance(field, str):
                            rlt[field] = eval("self.obj." + "{}".format(field))
                        else:
                            rlt[field[1]] = eval("self.obj." + "{}".format(field[0]))
                    self.context["data"] = rlt
                else:
                    self.context["data"] = self.obj
            else:
                self.template = "public/error.html"
        return super().get(request)

    # 封装post
    # "status",
    # 当前model的字段，关联的model, 类型， 反向关联的字段
    # ["content", "Content", "foreign_key", "article_id"],
    # ["tags", "Tag", "many2many"]
    # 如果传了时间，改为当前时间
    def post(self, request):
        cur_model_data_dict = {}
        foreign_key_sql_list = []
        many2many_sql_list = []
        for data in self.post_data:
            if isinstance(data, str):
                if re.search("time", data):
                    cur_model_data_dict[data] = datetime.now().strftime(DATETIME_FORMAT)
                elif re.search("password", data):
                    password = request.POST.get(data)
                    cur_model_data_dict[data] = functions.my_md5(flag=1, password=password)
                elif re.search("adder", data):
                    cur_model_data_dict[data] = self.admin_id
                else:
                    cur_model_data_dict[data] = int(request.POST.get(data)) if "id" in data else request.POST.get(data)
            else:
                if data[2] == "foreign_key":
                    foreign_data = request.POST.get(data[0])
                    foreign_key_sql_list.append(
                        data[1] + ".objects.create(" + data[0] + "='" + foreign_data + "', " + data[3] + "={})")
                else:
                    foreign_data = request.POST.get(data[0])
                    if len(foreign_data.split(',')) == 1:
                        many2many_sql_list.append("obj." + data[0] + ".add(" + foreign_data + ")")
                    else:
                        for many2many_id in eval(foreign_data):
                            many2many_sql_list.append("obj." + data[0] + ".add(" + str(many2many_id) + ")")
        try:
            if self.not_same:
                cur_model_data_dict.update({"is_deleted": 0})
                if self.model.objects.filter(**cur_model_data_dict):
                    self.context["code"] = "400"
                    self.context["msg"] = "已存在"
                    return super().post(request)
            obj = self.model.objects.create(**cur_model_data_dict)
            for foreign_key_sql in foreign_key_sql_list:
                eval(foreign_key_sql.format(obj.id))
            for many2many_sql in many2many_sql_list:
                eval(many2many_sql)
            try:
                name = obj.name
            except Exception:
                name = obj.title
            log.send(sender=self.model, admin=self.admin_info["admin_name"],
                     model=str(self.model), method="添加", name=name)
            self.context["obj_id"] = obj.id
            self.context["code"] = "200"
            self.context["msg"] = "添加成功"
        except Exception as e:
            self.context["code"] = "400"
            self.context['msg'] = "请求参数错误"
            pass
        return super().post(request)

    def delete(self, request):
        deleted_data = QueryDict(request.body)
        self.obj_id = deleted_data.get("id")
        check = self.model.objects.filter(id=int(self.obj_id))
        if check:
            self.obj = check.first()
            self.obj.is_deleted = 1
            try:
                self.obj.status = 1
                self.obj.pub_time = datetime.now().strftime(settings.DATETIME_FORMAT)
            except Exception:
                pass
            self.obj.save()
            try:
                name = self.obj.name
            except Exception:
                name = self.obj.title
            log.send(sender=self.model, admin=self.admin_info["admin_name"], model=str(self.model),
                     method="删除", name=name)
            self.context["code"] = "200"
            self.context["msg"] = "删除成功"
        else:
            self.context["code"] = "400"
            self.context["msg"] = "请求参数错误"
        return super().delete(request)

    def put(self, request):
        put_data = QueryDict(request.body)
        self.obj_id = put_data.get("id")
        cur_model_data_dict = {}
        foreign_key_sql_list = []
        many2many_sql_list = []
        for data in self.put_data:
            # "status",
            # 当前model的字段，关联的model, 类型， 反向关联的字段
            # ["content", "Content", "foreign_key", "article_id"],
            # ["tags", "Tag", "many2many"]
            if isinstance(data, str):
                if re.search("time", data):
                    cur_model_data_dict[data] = datetime.now().strftime(DATETIME_FORMAT)
                elif re.search("password", data):
                    password = put_data.get(data)
                    if password:
                        cur_model_data_dict[data] = functions.my_md5(flag=1, password=password)
                elif re.search("adder", data):
                    cur_model_data_dict[data] = self.admin_id
                else:
                    cur_model_data_dict[data] = int(put_data.get(data)) if "id" in data else put_data.get(data)
                if re.search("status", data):
                    if put_data.get(data) == '4':
                        try:
                            FeedBack.objects.filter(article_id=self.obj_id).update(feed_back=0)
                            Comment.objects.filter(article_id=self.obj_id).update(is_deleted=1)
                        except Exception:
                            pass
            else:
                foreign_data = put_data.get(data[0])
                if data[2] == "foreign_key":
                    foreign_key_sql_list.append(
                        data[1] + ".objects.filter(" + data[3] + " = {}" + ").update("
                        + data[0] + "='" + foreign_data + "')"
                    )
                else:
                    start = "self.model.objects.get(id=self.obj_id)." + data[0] + ".clear()"
                    each = []
                    if len(foreign_data.split(',')) == 1:
                        each.append(foreign_data)
                    else:
                        for many2many_id in eval(foreign_data):
                            each.append(many2many_id)
                    many2many_sql_list.append((start, data[0], each))
        try:
            obj2update = self.model.objects.filter(id=self.obj_id)
            obj = obj2update.first()
            obj2update.update(**cur_model_data_dict)
            for foreign_key_sql in foreign_key_sql_list:
                eval(foreign_key_sql.format(obj.id))
            for many2many_sql in many2many_sql_list:
                eval(many2many_sql[0])
                eval("obj.{}.add(*{})".format(many2many_sql[1], many2many_sql[2]))
            try:
                name = obj.name
            except Exception:
                name = obj.title
            log.send(sender=str(self.model), admin=self.admin_info["admin_name"],
                     model=str(self.model), method="修改",
                     name=name)
            self.context["code"] = "200"
            self.context["msg"] = "修改成功"
        except Exception as e:
            self.context["code"] = "400"
            self.context['msg'] = "已存在"
            pass
        return super().post(request)


class FrontMixin(object):
    def __init__(self):
        self.ip = None
        self.template = ''
        self.user_info = {}
        self.context = {}
        self.is_ajax = 0
        self.error = {}
        self.count = None
        self.url = "/article/draft/"
        self.if_has_right = False
        self.method = None
        self.admin_id = None
        self.is_sysop = False
        self.if_list = True
        self.user_id = None
        self.redirect = None

    def check_method(self, request):
        if self.error:
            return render(request, self.template, self.error)
        self.context.update({"count": self.count})
        if self.is_ajax == 0:
            return render(request, self.template, self.context)
        else:
            try:
                self.context["data"] = list(self.context["data"])
            except KeyError:
                pass
            return JsonResponse(self.context, safe=False)

    def pre_get(self, request):
        pass

    def get(self, request):
        self.pre_get(request)
        rlt = self.check_method(request)
        return rlt

    def pre_post(self, request):
        pass

    def post(self, request):
        self.pre_post(request)
        rlt = self.check_method(request)
        return rlt

    def pre_delete(self, request):
        pass

    def delete(self, request):
        self.pre_delete(request)
        rlt = self.check_method(request)
        return rlt

    def pre_put(self, request):
        pass

    def put(self, request):
        self.pre_delete(request)
        rlt = self.check_method(request)
        return rlt

    def check_if_list(self, request):
        if_list = request.GET.get("id", "")
        if if_list:
            self.if_list = False
        else:
            self.if_list = True

    def initialize(self, request):
        if 'user_info' not in request.session or "user_name" not in request.COOKIES:
            if self.url in [url[0] for url in settings.WHITE_URL]:
                self.context.update({"user_info": ""})
            else:
                self.redirect = "/user/login/"
        else:
            self.user_id = request.session["user_info"]["user_id"]
            self.context.update(request.session['user_info'])

    def dispatch(self, request, *args, **kwargs):
        self.url = request.path
        self.initialize(request)
        if self.redirect:
            return HttpResponse(json.dumps({"code": 403, "msg": "未登录"}))
        if self.template:
            return render(request, self.template)
        self.check_if_list(request)
        return super().dispatch(request, *args, **kwargs)


class FrontLoggedMixin(FrontMixin, View):
    def __init__(self):
        super().__init__()
        self.model = None
        # 当前对象id
        self.obj_id = None
        # {filed: condition}
        self.or_field = {}
        self.and_field = {}
        # 列表展示的字段
        self.list_values = []
        # 详情展示的字段
        self.detail_values = []
        # 分页后的查询结果集
        self.page_query_set = None
        # 当前对象
        self.obj = None
        # 要搜索的字段
        self.search_field = None
        # post请求时发送的字段
        self.post_data = []
        # put请求时发送的字段
        self.put_data = []
        # 展示详情时获取哪个字段以获取信息
        self.detail_id_field = "id"
        # 是否需要分页
        self.need_page = True

    def get_page(self, request, query_set):
        page = request.GET.get('page', '')
        size = request.GET.get('size', '')
        order = request.GET.get('order', 'pub_time')
        search = request.GET.get('search', '')
        rlt_and_field = []
        rlt_or_field = []
        if search:
            for field in self.search_field:
                rlt_or_field.append('Q(%s__icontains="%s")' % (field, search))
        for field, condition in self.or_field.items():
            if isinstance(condition, int):
                rlt_or_field.append('Q(%s=%s)' % (field, condition))
            else:
                rlt_or_field.append('Q(%s="%s")' % (field, condition))
        for field, condition in self.and_field.items():
            if isinstance(condition, int):
                rlt_and_field.append('Q(%s=%s)' % (field, condition))
            else:
                rlt_and_field.append('Q(%s="%s")' % (field, condition))
        if rlt_or_field:
            str_or_filter = ' | '.join(rlt_or_field) + ' & '
        else:
            str_or_filter = ""
        str_and_filter = ' & '.join(rlt_and_field)
        condition = str_or_filter + str_and_filter
        if condition:
            query_set = query_set.filter(eval(condition))
        if not order:
            order = "pub_time"
        order_type = request.GET.get('type', 'desc')
        if order_type == "desc":
            order = "-" + order
        if not page:
            page = 1
        if not size:
            size = 3
        page = int(page)
        size = int(size)
        self.count = query_set.count()
        self.page = page
        if self.count:
            page_num = self.count // size if self.count % size == 0 else self.count//size+1
            if page_num <= 9:
                show_page = {"show_page": [i+1 for i in range(page_num)]}
            elif self.page < 5:
                show_page = {"show_page": [i+1 for i in range(9)]}
            elif page_num - self.page < 5:
                show_page = {"show_page": [i+1 for i in range(page_num)[-9:]]}
            else:
                show_page = {"show_page": [i for i in range(self.page-4, self.page+5)]}
            self.context.update(show_page)
            self.context.update({"cur_page": self.page})
            self.context.update({"count": self.count})
            self.context.update({"page_num": page_num})
        self.page_query_set = query_set.order_by(order)[(self.page - 1) * size:(self.page - 1) * size + size]

    def get(self, request):
        self.obj_id = request.GET.get('id', '')
        if not self.obj_id:
            query_set = self.model.objects.all()
            self.get_page(request, query_set)
            all_field_dict = {}
            all_field_list = []
            for field in self.list_values:
                # "reject_reason",
                # ["adder__name", "adder_name"],
                if isinstance(field, str):
                    all_field_list.append(field)
                else:
                    # 重命名
                    all_field_dict[field[1]] = F(field[0])
            if self.need_page:
                if self.list_values:
                    self.context["data"] = self.page_query_set.values(*all_field_list, **all_field_dict)
                else:
                    self.context["data"] = self.page_query_set
            else:
                if self.list_values:
                    self.context["data"] = query_set.values(*all_field_list, **all_field_dict)
                else:
                    self.context["data"] = query_set
        else:
            self.obj_id = int(self.obj_id)
            filter_dict = {self.detail_id_field: self.obj_id}
            check = self.model.objects.filter(**filter_dict)
            if check:
                self.obj = check.first()
                rlt = {}
                if self.detail_values:
                    for field in self.detail_values:
                        # "content",
                        # ["article.tags.all().values('name', 'id')", "tags"],
                        if isinstance(field, str):
                            rlt[field] = eval("self.obj." + "{}".format(field))
                        else:
                            rlt[field[1]] = eval("self.obj." + "{}".format(field[0]))
                    self.context["data"] = rlt
                else:
                    self.context["data"] = self.obj
            else:
                self.error["code"] = "404"
                self.error["msg"] = "404 Not Found 未找到"
                self.template = "public/error.html"
        return super().get(request)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
