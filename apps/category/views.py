import json

from django.http import QueryDict, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from common.models import Category, Article
from utils.common_mixin import AdminLoggedMixin


class CategoryView(AdminLoggedMixin, View):
    def get(self, request):
        self.model = Category
        self.and_field = {"is_deleted": 0}
        self.template = "category/category_list.html"
        self.need_page = False
        return super().get(request)

    def post(self, request):
        self.model = Category
        self.post_data = ["name"]
        self.is_ajax = 1
        self.not_same = True
        return super().post(request)

    def delete(self, request):
        self.model = Category
        self.is_ajax = 1
        return super().delete(request)