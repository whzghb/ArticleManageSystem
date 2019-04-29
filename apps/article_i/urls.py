from django.urls import path
from article_i import views

urlpatterns = [
    path('draft/', views.ArticleView.as_view(), name="article_draft"),
    path('to_audit/', views.ArticleView.as_view(), name="article_to_audit"),
    path('to_publish/', views.ArticleView.as_view(), name="article_to_publish"),
    path('published/', views.ArticleView.as_view(), name="article_published"),
    path('rejected/', views.ArticleView.as_view(), name="article_rejected"),
    path('error/', views.ArticleView.as_view(), name="article_error"),
    path('add/', views.ArticleAddView.as_view(), name="article_add"),
    path('edit/', views.ArticleEditView.as_view(), name="article_edit"),
    path('s_c/reject/', views.ArticleStatusChange.as_view(), name="reject"),
    path('s_c/back/', views.ArticleStatusChange.as_view(), name="back"),
    path('s_c/publish/', views.ArticleStatusChange.as_view(), name="back"),
    path('s_c/permit/', views.ArticleStatusChange.as_view(), name="permit"),
    path('s_c/to_audit/', views.ArticleStatusChange.as_view(), name="to_audit")
]