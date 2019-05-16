from django.urls import path
from common import views

urlpatterns = [
    path('uploads/img/', views.UploadsImgView.as_view()),
    path('comment/admin_del/', views.CommentAdminDel.as_view()),
    path('comment/user_del/', views.CommentUserDel.as_view()),
    path('video/', views.VideoView.as_view()),
]