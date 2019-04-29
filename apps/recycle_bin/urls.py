from django.urls import path
from recycle_bin import views

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article_recy"),
]