# Create your views here.
from collections import defaultdict
from django.views import View
from common.models import Position, Right
from utils.common_mixin import AdminLoggedMixin, AdminMixin


class PositionView(AdminLoggedMixin, View):
    def get_template(self, request):
        if self.if_list:
            self.template = "position/list.html"
        else:
            rights = Right.objects.all().values("id", "action_group_id", "action_group__group", "action")
            res = defaultdict(list)
            for right in rights:
                res[right['action_group_id']].append((right['id'], right['action_group__group'], right['action']))
            self.context.update({"rights": dict(res)})
            self.template = "position/detail.html"

    def get(self, request):
        self.model = Position
        self.list_values = [
            "id",
            "name",
            "add_time"
        ]
        self.detail_values = [
            "id",
            "name",
            ["rights.all().values_list('id', flat=True)", "rights"]
        ]
        self.and_field = {"is_deleted": 0}
        self.get_template(request)
        return super().get(request)

    def post(self, request):
        self.model = Position
        self.is_ajax = 1
        self.post_data = [
            "name",
            ["rights", "Right", "many2many"]
        ]
        return super().post(request)

    def put(self, request):
        self.model = Position
        self.is_ajax = 1
        self.put_data = [
            "name",
            ["rights", "Right", "many2many"]
        ]
        return super().put(request)

    def delete(self, request):
        self.model = Position
        self.is_ajax = 1
        return super().delete(request)


class PositionAddView(AdminMixin, View):
    def get(self, request):
        rights = Right.objects.all().values("id", "action_group_id", "action_group__group", "action")
        res = defaultdict(list)
        for right in rights:
            res[right['action_group_id']].append((right['id'], right['action_group__group'], right['action']))
        self.context.update({"rights": dict(res)})
        self.template = "position/add.html"
        return super().get(request)


class PositionAjax(AdminMixin, View):
    def get(self, request):
        self.is_ajax = 1
        rights = Position.objects.get(id=self.obj_id).rights.all().values_list("id", flat=True)
        self.context.update({"rights": list(rights)})
        return super().get(request)

