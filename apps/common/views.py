import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View
from celery_tasks import tasks
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


class VideoView(AdminMixin, View):
    def request_2_json(self):
        return self.request.__dict__

    def get(self, request):
        name = request.GET.get("name")
        self.template = 'common/iframe_movie.html'
        self.context = {"name": name}
        return super().get(request)

    def post(self, request):
        self.is_ajax = 1
        # <iframe style="width: 500px; height: 290px; overflow: hidden" src="http://127.0.0.1:9000/common/video?name=n0754qi98ej.mp4"></iframe>
        name = tasks.write_video(request, "video")
        url = '<iframe style="width: 500px; height: 290px; overflow: hidden" ' \
              'src="{}"></iframe>'.format(name)
        print(url)
        self.context.update({"url": url})
        return super().post(request)





