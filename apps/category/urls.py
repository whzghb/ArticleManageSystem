from django.urls import path
from category import views

urlpatterns = [
    path('', views.CategoryView.as_view(), name='category'),
]