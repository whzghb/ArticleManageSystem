import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View

from common.models import Comment
from utils import functions
from utils.common_mixin import AdminMixin, FrontMixin
from utils.signal import log


class UploadsImgView(AdminMixin, View):
    def post(self, request):
        self.is_ajax = 1
        url = functions.write_file(request, "img")
        self.context.update({"data": [url], "errno": 0})
        return super().post(request)


class CommentAdminDel(AdminMixin, View):
    def post(self, request):
        id = request.POST.get("id")
        obj = Comment.objects.get(id=id)
        if obj.is_deleted == 2:
            obj.is_deleted = 0
            log.send(sender="Comment", admin=self.admin_info["admin_name"],
                     model="Comment", method="恢复",
                     name=obj.content)
        else:
            obj.is_deleted = 2
            log.send(sender="Comment", admin=self.admin_info["admin_name"],
                     model="Comment", method="删除",
                     name=obj.content)
        obj.save()
        self.is_ajax = 1
        return super().get(request)


class CommentUserDel(FrontMixin, View):
    def get(self, request):
        id = request.GET.get("id")
        obj = Comment.objects.get(id=id)
        obj.is_deleted = 1
        obj.save()
        self.is_ajax = 1
        return super().get(request)

