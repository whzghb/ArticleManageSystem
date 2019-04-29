"""ArticleManageSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    path('admin/analysis/', include('data.urls'), name='data'),
    path('admin/article_i/', include('article_i.urls'), name='article'),
    path('article/', include('article_o.urls'), name='article_o'),
    path('admin/category/', include('category.urls'), name='category'),
    path('admin/recycle_bin/', include('recycle_bin.urls'), name='recycle_bin'),
    path('admin/tag/', include('tag.urls'), name='tag'),
    path('admin/user/', include("user_i.urls"), name="user_i"),
    path('user/', include('user.urls'), name='user'),
    path('system/', include('system.urls'), name='system'),
    path('admin/', include('admin.urls'), name='admin'),
    path('common/', include("common.urls"), name="common"),
    path('', include("article_o.urls"), name="outer"),

]
