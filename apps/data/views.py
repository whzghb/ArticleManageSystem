import datetime

from django.db import connection
from django.shortcuts import render

# Create your views here.
# Article
from django.views import View

from common.models import Article, Comment, FeedBack, Content, User, Log, CommentFeedBack
from utils.common_mixin import AdminMixin, AdminLoggedMixin


class ArticleAnalyseView(AdminLoggedMixin, View):
    def get_extra_fields(self, request):
        if self.if_list:
            self.model = Article
            self.template = "data/article_list.html"
        else:
            self.model = Content
            self.template = "data/article_ana_detail.html"
            id = self.request.GET.get("id")
            good_view = FeedBack.objects.filter(article_id=id, feed_back=1).count()
            bad_view = FeedBack.objects.filter(article_id=id, feed_back=2).count()
            comments = Comment.objects.filter(article_id=id)
            for comment in comments:
                comment.good_view = CommentFeedBack.objects.filter(comment_id=comment.id, feed_back=1).count()
                comment.bad_view = CommentFeedBack.objects.filter(comment_id=comment.id, feed_back=2).count()
            count = comments.count()
            extra = {}
            extra["article_id"] = id
            extra["good_view"] = good_view
            extra["bad_view"] = bad_view
            extra["comments"] = comments
            extra["count"] = count
            self.context.update(extra)

    def get(self, request):
        self.list_values = [
            "id",
            "title",
            ["adder__name", "adder_name"],
            ["category__name", "category_name"],
            "add_time",
            "read_times",
            "last_read_time",
        ]
        self.detail_values = [
            "content",
            ["article.title", "title"],
            ["article_id", "id"],
            ["article.category.name", "category"], ["article.tags.all().values('name', 'id')", "tags"],
            ["article.author", "author"]
        ]
        self.and_field = {"is_deleted": 0, "status": 4}
        self.detail_id_field = "article_id"
        self.get_extra_fields(request)
        self.search_field = ["title", "adder__name", "category__name"]
        return super().get(request)


class UserAnalyseView(AdminMixin, View):
    def get(self, request):
        sql1 = "SELECT COUNT(0) FROM common_user WHERE register_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE register_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE register_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE register_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE register_time > '%s' " % (
                    datetime.date.today(),
                    datetime.date.today() - datetime.timedelta(days=3),
                    datetime.date.today() - datetime.timedelta(days=7),
                    datetime.date.today() - datetime.timedelta(days=15),
                    datetime.date.today() - datetime.timedelta(days=30),
                )
        sql2 = "SELECT COUNT(0) FROM common_user WHERE last_log_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE last_log_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE last_log_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE last_log_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_user WHERE last_log_time > '%s' " % (
                   datetime.date.today(),
                   datetime.date.today() - datetime.timedelta(days=3),
                   datetime.date.today() - datetime.timedelta(days=7),
                   datetime.date.today() - datetime.timedelta(days=15),
                   datetime.date.today() - datetime.timedelta(days=30),
               )
        sql3 = "SELECT COUNT(0) FROM common_feedback WHERE add_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_feedback WHERE add_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_feedback WHERE add_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_feedback WHERE add_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_feedback WHERE add_time > '%s' " % (
                   datetime.date.today(),
                   datetime.date.today() - datetime.timedelta(days=3),
                   datetime.date.today() - datetime.timedelta(days=7),
                   datetime.date.today() - datetime.timedelta(days=15),
                   datetime.date.today() - datetime.timedelta(days=30),
               )
        sql4 = "SELECT COUNT(0) FROM common_comment WHERE comment_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_comment WHERE comment_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_comment WHERE comment_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_comment WHERE comment_time > '%s' " \
               "UNION SELECT COUNT(0) FROM common_comment WHERE comment_time > '%s' " % (
                   datetime.date.today(),
                   datetime.date.today() - datetime.timedelta(days=3),
                   datetime.date.today() - datetime.timedelta(days=7),
                   datetime.date.today() - datetime.timedelta(days=15),
                   datetime.date.today() - datetime.timedelta(days=30),
               )
        cursor = connection.cursor()
        cursor.execute(sql1)
        count_reg = cursor.fetchall()

        cursor.execute(sql2)
        count_last_log = cursor.fetchall()

        cursor.execute(sql3)
        count_feedback = cursor.fetchall()

        cursor.execute(sql4)
        count_comment = cursor.fetchall()

        count_reg = list(map(lambda t: t[0], count_reg))
        while len(count_reg) < 5:
            count_reg.append(count_reg[-1])

        count_last_log = list(map(lambda t: t[0], count_last_log))
        while len(count_last_log) < 5:
            count_last_log.append(count_last_log[-1])

        count_feedback = list(map(lambda t: t[0], count_feedback))
        while len(count_feedback) < 5:
            count_feedback.append(count_feedback[-1])

        count_comment = list(map(lambda t: t[0], count_comment))
        while len(count_comment) < 5:
            count_comment.append(count_comment[-1])
        self.template = "data/user.html"
        self.context.update({
            "count_reg": count_reg,
            "count_last_log": count_last_log,
            "count_feedback": count_feedback,
            "count_comment": count_comment
        })
        return super().get(request)


class LogView(AdminLoggedMixin, View):
    def get(self, request):
        self.model = Log
        self.template = "data/log_list.html"
        self.search_field = ["model", "method", "admin", "name"]
        return super().get(request)

