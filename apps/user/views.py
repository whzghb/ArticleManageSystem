import datetime
import json
import re

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ArticleManageSystem import settings
from common.models import User
from utils import functions
from utils.common_mixin import FrontLoggedMixin, FrontMixin
from ArticleManageSystem.settings import DATETIME_FORMAT

# Create your views here.
from django.views import View


class LoginView(View):
    def __init__(self):
        super().__init__()
        self.context = {}
        self.user_info = {}

    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        name = request.POST.get("name")
        password = request.POST.get("password")
        md5_passwd = functions.my_md5(flag=1, password=password)
        check = User.objects.filter(name=name, password=md5_passwd, is_deleted=0)
        if not check:
            self.context["error"] = "用户名或密码错误"
            self.context["code"] = 400
        else:
            obj = check.first()
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            obj.log_times += 1
            obj.last_log_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
            obj.last_log_ip = ip
            obj.save()
            self.user_info["user_name"] = obj.name
            self.user_info["user_id"] = obj.id
            request.session["user_info"] = self.user_info
            self.context["msg"] = "登录成功"
            self.context["code"] = 200
            response = HttpResponse(json.dumps(self.context))
            response.set_cookie("user_name", json.dumps(obj.name))
            response.set_cookie("user_id", obj.id)
            return response
        return HttpResponse(json.dumps(self.context))


class RegisterView(View):
    def __init__(self):
        super().__init__()
        self.context = {}
        self.user_info = {}

    def get(self, request):
        return render(request, "user/register.html")

    def check_invalid_name(self, name):
        for i in settings.ERROR_CHAR:
            if i in name:
                return False
        return True

    def post(self, request):
        name = request.POST.get("name")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if User.objects.filter(name=name):
            self.context["error"] = "用户已存在"
            self.context["code"] = 400
        elif password != re_password:
            self.context["error"] = "两次密码不一致"
            self.context["code"] = 400
        elif len(name) > 30:
            self.context["error"] = "用户名过长"
            self.context["code"] = 400
        elif not self.check_invalid_name(name):
            self.context["error"] = "用户名包含特殊字符"
            self.context["code"] = 400
        elif len(password) < 6:
            self.context["error"] = "密码长度必须大于6位"
            self.context["code"] = 400
        else:
            md5_passwd = functions.my_md5(flag=1, password=password)
            obj = User.objects.create(name=name,
                                      password=md5_passwd,
                                      register_time=datetime.datetime.now().strftime(DATETIME_FORMAT))
            self.context["msg"] = "注册成功"
            self.context["code"] = 200
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            obj.log_times += 1
            obj.last_log_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
            obj.last_log_ip = ip
            obj.save()
            self.user_info["user_name"] = obj.name
            self.user_info["user_id"] = obj.id
            request.session["user_info"] = self.user_info
            self.context["msg"] = "登录成功"
            self.context["code"] = 200
            response = HttpResponse(json.dumps(self.context))
            response.set_cookie("user_name", json.dumps(obj.name))
            response.set_cookie("user_id", obj.id)
            return response
        return HttpResponse(json.dumps(self.context))


class LogoutView(FrontMixin, View):
    def get(self, request):
        del request.session["user_info"]
        response = HttpResponseRedirect('/')
        response.delete_cookie('user_name')
        response.delete_cookie('user_id')
        return response
