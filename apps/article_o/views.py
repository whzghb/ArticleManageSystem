import random
from datetime import datetime

from django.core.cache import cache
from django.db import connection
from django.db.models import Q, Count
from django.shortcuts import render

# Create your views here.
from django.views import View
from ArticleManageSystem.settings import DATETIME_FORMAT
from common.models import Article, Content, FeedBack, Comment, Tag, CommentFeedBack
from utils.common_mixin import FrontLoggedMixin, FrontMixin


class UserArticleView(FrontLoggedMixin, View):
    def get_template(self):
        if self.if_list:
            self.model = Article
            page = self.request.GET.get("page")
            if not page:
                most_hot = Article.objects.filter(is_deleted=0,
                                                  status=4).values("title", "id").order_by("-read_times")[:5]
                most_comment = Comment.objects.filter(article__is_deleted=0, article__status=4)\
                    .values("article__title", "article_id").annotate(count=Count("article_id")).order_by("-count")[:5]
                self.context.update({"most_hot": most_hot, "most_comment": most_comment})
            self.template = "article_o/article_list_add.html"
        else:
            id = self.request.GET.get("id")
            id = int(id)
            self.model = Content
            self.template = "article_o/article_detail_4.html"
            good_view = FeedBack.objects.filter(article_id=id, feed_back=1).count()
            bad_view = FeedBack.objects.filter(article_id=id, feed_back=2).count()
            comments = Comment.objects.filter(article_id=id)
            for comment in comments:
                comment.good_view = CommentFeedBack.objects.filter(comment_id=comment.id, feed_back=1).count()
                comment.bad_view = CommentFeedBack.objects.filter(comment_id=comment.id, feed_back=2).count()
            comm_count = comments.count()
            this_tags = tuple(Article.objects.get(id=id).tags.all().values_list("id", flat=True))
            sql = "SELECT distinct a.id, a.title FROM common_article a left join common_article_tags t " \
                  "on a.id = t.article_id WHERE t.tag_id in %s and a.id != %s and a.status=4 and is_deleted=0"
            cursor = connection.cursor()
            cursor.execute(sql, [this_tags, id])
            if_like = list(cursor.fetchall())
            random.shuffle(if_like)
            extra = {}
            extra["if_like"] = if_like[:4]
            extra["article_id"] = id
            extra["good_view"] = good_view
            extra["bad_view"] = bad_view
            extra["comments"] = comments
            extra["comm_count"] = comm_count
            self.context.update(extra)

    def get_list_values(self):
        """
        如果不需要重命名就用字符串，否则前面写跨表的方式，values跨表用双下划线，后面写要改的名字
        """
        self.list_values = [
            "id",
            "img",
            "title",
            "author",
            "pub_time",
            ["category__name", "category_name"],
            # ["content__content", "content_val"],
        ]

    def get_detail_values(self):
        """
        如果不需要重命名就用字符串，否则前面写跨表的方式，详情跨表用点，后面写要改的名字
        """
        self.detail_values = [
            "content",
            ["article.title", "title"],
            ["article_id", "id"],
            ["article.category.name", "category"], ["article.tags.all().values('name', 'id')", "tags"],
            ["article.author", "author"]
        ]

    def get_change(self, request):
        if not self.if_list:
            obj_id = request.GET.get("id")
            try:
                obj = Article.objects.get(id=obj_id)
            except Exception:
                self.template = "public/error.html"
            else:
                obj.read_times += 1
                obj.last_read_time = datetime.now().strftime(DATETIME_FORMAT)
                obj.save()

    def get(self, request):
        cur_page = request.GET.get("page", "1")
        if cur_page != "1":
            self.is_ajax = 1
        self.and_field = {"status": 4, "is_deleted": 0}
        self.detail_id_field = "article_id"
        self.get_list_values()
        self.get_detail_values()
        self.get_change(request)
        if self.template:
            return render(request, self.template)
        self.get_template()
        return super().get(request)


class DianZan(FrontMixin, View):
    def post(self, request):
        id = request.POST.get("id")
        view = int(request.POST.get("view"))
        extra = {}
        extra["is_view"] = 0
        user = self.user_id
        check = FeedBack.objects.filter(article_id=id, user_id=user)
        if check:
            obj = check.first()
            if obj.feed_back == view:
                extra["is_view"] = 1
            else:
                obj.feed_back = view
            obj.save()
        else:
            FeedBack.objects.create(article_id=id, user_id=user, feed_back=view)
        self.is_ajax = 1
        good_view = FeedBack.objects.filter(article_id=id, feed_back=1).count()
        bad_view = FeedBack.objects.filter(article_id=id, feed_back=2).count()
        extra["good_view"] = good_view
        extra["bad_view"] = bad_view
        self.context.update(extra)
        return super().post(request)


class CommentView(FrontMixin, View):
    def post(self, request):
        user = self.user_id
        id = request.POST.get("id")
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        Comment.objects.create(article_id=id, parent_comment_id=parent_id, content=content, user_id=user)
        extra = {}
        extra["comments"] = Comment.objects.filter(article_id=id)
        self.is_ajax = 1
        return super().post(request)


class CommentDianZan(FrontMixin, View):
    def post(self, request):
        id = request.POST.get("id")
        view = int(request.POST.get("view"))
        extra = {}
        extra["is_view"] = 0
        user_id = self.user_id
        check = CommentFeedBack.objects.filter(comment_id=id, user_id=user_id)
        if check:
            obj = check.first()
            if obj.feed_back == view:
                extra["is_view"] = 1
            else:
                obj.feed_back = view
            obj.save()
        else:
            CommentFeedBack.objects.create(comment_id=id, user_id=user_id, feed_back=view)
        self.is_ajax = 1
        good_view = CommentFeedBack.objects.filter(comment_id=id, feed_back=1).count()
        bad_view = CommentFeedBack.objects.filter(comment_id=id, feed_back=2).count()
        extra["good_view"] = good_view
        extra["bad_view"] = bad_view
        self.context.update(extra)
        return super().post(request)
