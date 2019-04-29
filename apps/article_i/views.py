# Create your views here.
import re
from datetime import datetime

from django.db import connection
from django.db.models import Count, F, Q
from django.views import View
from utils.common_mixin import AdminLoggedMixin, AdminMixin
from common.models import Article, Content, Category, Tag, FeedBack
from ArticleManageSystem.settings import DATETIME_FORMAT
from utils.functions import get_page


class ArticleView(AdminLoggedMixin, View):
    def get_model(self, request):
        self.if_list = request.GET.get("id", 0)
        if self.if_list == 0:
            self.model = Article
        else:
            self.model = Content

    def get_error_article(self, request):
        search = request.GET.get('search', "")
        if not search:
            feed_back = FeedBack.objects.filter(Q(article__status=4) & Q(article__is_deleted=0) & Q(feed_back__gt=0)) \
                .values("article_id", "feed_back", title=F("article__title"), adder=F("article__adder__name"),
                        pub_time=F("article__pub_time")) \
                .annotate(count=Count("article"))
        else:
            feed_back = FeedBack.objects.filter(
                Q(article__status=4) & Q(article__is_deleted=0) &
                (Q(article__title__icontains=search) & Q(feed_back__gt=0) | Q(article__adder__name=search))) \
                .values("article_id", "feed_back", title=F("article__title"), adder=F("article__adder__name"),
                        pub_time=F("article__pub_time")) \
                .annotate(count=Count("article"))
        from collections import defaultdict
        dic = defaultdict(list)
        for fd in feed_back:
            dic[fd["article_id"]].append([fd["feed_back"], fd["count"], fd["adder"], fd["pub_time"], fd["title"]])
        res = {}
        for key, value in dic.items():
            if len(value) == 1:
                if value[0][0] == 2:
                    b_c = value[0][1]
                    g_c = 0
                    value[0].extend([g_c, b_c])
                    res[key] = value[0][2:]
            else:
                if value[0][0] == 2:
                    if value[0][1] > value[1][1]:
                        b_c = value[0][1]
                        g_c = value[1][1]
                        value[0].extend([g_c, b_c])
                        res[key] = value[0][2:]
                else:
                    if value[1][1] > value[0][1]:
                        b_c = value[1][1]
                        g_c = value[0][1]
                        value[0].extend([g_c, b_c])
                        res[key] = value[0][2:]
        res = get_page(self, request, res)
        self.context.update({"res": res, "title": "异常文章"})
        self.need_page = False

    def get_extra_fields(self, request):
        if "/admin/article_i/draft/" == self.url:
            self.context.update({"title": "草稿箱"})
            status = 1
        elif "/admin/article_i/to_audit/" == self.url:
            self.context.update({"title": "待审核"})
            status = 2
        elif "/admin/article_i/to_publish/" == self.url:
            self.context.update({"title": "待发布"})
            status = 3
        elif "/admin/article_i/published/" == self.url:
            self.context.update({"title": "已发布"})
            status = 4
        elif "/admin/article_i/rejected/" == self.url:
            self.context.update({"title": "已驳回"})
            status = 5
        else:
            self.get_error_article(request)
            status = 10
        self.and_field.update({"status": status})

    def get_template(self, request):
        if_list = request.GET.get("id", 0)
        if if_list == 0:
            if "/admin/article_i/published/" == self.url:
                self.template = "article/published_list.html"
            elif "/admin/article_i/error/" == self.url:
                self.template = "article/error_list.html"
            else:
                self.template = "article/article_list.html"
        else:
            if "/admin/article_i/draft/" == self.url:
                self.template = "article/article_detail.html"
            elif "/admin/article_i/to_audit/" == self.url:
                self.template = "article/audit.html"
            elif "/admin/article_i/to_publish/" == self.url:
                self.template = "article/to_publish.html"
            elif "/admin/article_i/published/" == self.url:
                self.template = "article/published.html"
            elif "/admin/article_i/rejected/" == self.url:
                self.template = "article/rejected.html"
            else:
                self.template = "article/published.html"

    def get_list_values(self):
        """
        如果不需要重命名就用字符串，否则前面写跨表的方式，values跨表用双下划线，后面写要改的名字
        """
        self.list_values = [
            "id",
            "title",
            "author",
            "add_time",
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
            "img",
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
        """
        条件为与的字段和条件
        """
        self.and_field = {"is_deleted": 0}

    def get(self, request):
        self.get_model(request)
        self.detail_id_field = "article_id"
        self.get_and_field()
        self.get_extra_fields(request)
        self.get_template(request)
        self.get_list_values()
        self.get_detail_values()
        self.search_field = ["title", "author", "category__name"]
        return super().get(request)

    def post(self, request):
        self.model = Article
        # self.get_template(request)
        self.get_post_data()
        self.is_ajax = 1
        return super().post(request)

    def put(self, request):
        self.model = Article
        self.put_data = [
            "img",
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
        self.is_ajax = 1
        return super().put(request)

    def delete(self, request):
        self.model = Article
        self.is_ajax = 1
        return super().delete(request)


class ArticleStatusChange(AdminLoggedMixin, View):
    def get_put_data(self):
        self.put_data = ["status", "reject_reason", "pub_time"]

    def put(self, request):
        self.model = Article
        self.is_ajax = 1
        self.get_put_data()
        return super().put(request)


class ArticleAddView(AdminMixin, View):
    def get(self, request):
        category = Category.objects.filter(is_deleted=0).values("id", "name")
        tag = Tag.objects.filter(is_deleted=0).values("id", "name")
        self.context.update({"category": category})
        self.context.update({"tag": tag})
        self.template = "article/article_add.html"
        return super().get(request)


class ArticleEditView(AdminLoggedMixin, View):
    def get_detail_values(self):
        self.detail_values = [
            "content",
            ["article.img", "img"],
            ["article.add_time", "add_time"],
            ["article.pub_time", "pub_time"],
            ["article.title", "title"],
            ["article_id", "id"],
            ["article.category.name", "category"], ["article.tags.all().values('name', 'id')", "tags"],
            ["article.author", "author"], ["article.adder.name", "adder"],
            ["article.category_id", "category_id"]
        ]

    def get(self, request):
        self.detail_id_field = "article_id"
        category = Category.objects.filter(is_deleted=0).values("id", "name")
        tag = Tag.objects.filter(is_deleted=0).values("id", "name")
        self.context.update({"category": category})
        self.context.update({"tag": tag})
        self.template = "article/edit.html"
        self.model = Content
        self.get_detail_values()
        return super().get(request)

