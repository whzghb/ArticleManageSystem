from django.urls import path
from data import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('article/', views.ArticleAnalyseView.as_view(), name="article_ana"),
    # path('user/', cache_page(60*10)(views.UserAnalyseView.as_view()), name="user_ana"),
    # path('log/', cache_page(60*10)(views.LogView.as_view()), name="log")
    path('user/', views.UserAnalyseView.as_view(), name="user_ana"),
    path('log/', views.LogView.as_view(), name="log")
]