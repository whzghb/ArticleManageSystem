# Create your views here.
import re
import datetime
from django.views import View
from utils.common_mixin import AdminLoggedMixin
from common.models import Article, Content


class ArticleView(AdminLoggedMixin, View):
    def get_model(self, request):
        self.if_list = request.GET.get("id", 0)
        if self.if_list == 0:
            self.model = Article
        else:
            self.model = Content

    def get_list_values(self):
        """
        如果不需要重命名就用字符串，否则前面写跨表的方式，values跨表用双下划线，后面写要改的名字
        """
        self.list_values = [
            "id",
            "title",
            "author",
            "pub_time",
            ["adder__name", "adder_name"],
            ["category__name", "category_name"]
        ]

    def get_detail_values(self):
        """
        如果不需要重命名就用字符串，否则前面写跨表的方式，详情跨表用点，后面写要改的名字
        """
        self.detail_values = [
            "content",
            ["article.reject_reason", "rejected_reason"],
            ["article.add_time", "add_time"],
            ["article.pub_time", "pub_time"],
            ["article.title", "title"],
            ["article_id", "id"],
            ["article.category.name", "category"], ["article.tags.all().values('name', 'id')", "tags"],
            ["article.author", "author"], ["article.adder.name", "adder"]
        ]

    def get_post_data(self):
        self.post_data = [
            "title",
            "author",
            "category_id",
            "adder_id",
            "pub_time",
            "status",
            # 当前model的字段，关联的model, 类型， 反向关联的字段
            ["content", "Content", "foreign_key", "article_id"],
            ["tags", "Tag", "many2many"]
        ]

    def get_and_field(self):
        self.and_field = {"is_deleted": 1, "pub_time__gt": datetime.datetime.now()-datetime.timedelta(days=30)}

    def get_template(self, request):
        if_list = request.GET.get("id", 0)
        if if_list == 0:
            self.template = "article/recycle_list.html"
        else:
            self.template = "article/recycle_detail.html"

    def get(self, request):
        self.get_model(request)
        self.detail_id_field = "article_id"
        self.get_and_field()
        self.get_list_values()
        self.get_detail_values()
        self.search_field = ["title", "author", "category__name"]
        self.get_template(request)
        return super().get(request)

    def put(self, request):
        self.model = Article
        self.is_ajax = 1
        self.put_data = [
            "id",
            "is_deleted"
        ]
        return super().put(request)



