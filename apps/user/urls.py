from django.urls import path
from user import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="user_login"),
    path('register/', views.RegisterView.as_view(), name="user_register"),
    path('logout/', views.LogoutView.as_view(), name="user_logout"),
]