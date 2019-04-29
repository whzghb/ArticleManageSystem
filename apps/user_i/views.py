from django.shortcuts import render
from django.views import View

from common.models import User
from utils.common_mixin import AdminLoggedMixin
# Create your views here.


class UserView(AdminLoggedMixin, View):
    def get_extra_fields(self, request):
        pass

    def get(self, request):
        self.list_values = [
            "id",
            "name",
            "register_time",
            "last_log_time",
            "log_times",
            "last_log_ip",
        ]
        self.template = "user_i/user_list.html"
        self.model = User
        self.and_field = {"is_deleted": 0}
        self.search_field = ["name"]
        return super().get(request)

    def delete(self, request):
        self.model = User
        self.is_ajax = 1
        return super().delete(request)
