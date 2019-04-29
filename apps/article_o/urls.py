from django.urls import path
from article_o import views

urlpatterns = [
    path("zan/", views.DianZan.as_view(), name="zan"),
    path("comment_zan/", views.CommentDianZan.as_view(), name="comment_zan"),
    path("comment/", views.CommentView.as_view(), name="comment"),
    path("", views.UserArticleView.as_view(), name="article"),
]