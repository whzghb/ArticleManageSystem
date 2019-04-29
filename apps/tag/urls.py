from django.urls import path
from tag import views

urlpatterns = [
    path('', views.TagView.as_view(), name="tag"),
]