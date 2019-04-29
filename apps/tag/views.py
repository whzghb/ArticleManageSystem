# Create your views here.
from django.views import View
from common.models import Tag
from utils.common_mixin import AdminLoggedMixin


class TagView(AdminLoggedMixin, View):
    def get(self, request):
        self.model = Tag
        self.and_field = {"is_deleted": 0}
        self.template = "tag/tag_list.html"
        self.need_page = False
        return super().get(request)

    def post(self, request):
        self.model = Tag
        self.post_data = ["name"]
        self.is_ajax = 1
        self.not_same = True
        return super().post(request)

    def delete(self, request):
        self.model = Tag
        self.is_ajax = 1
        return super().delete(request)