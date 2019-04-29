from django.urls import path
from admin import views

urlpatterns = [
    path('add/', views.AdminAdd.as_view(), name="admin_add"),
    path('login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('main/', views.MainView.as_view(), name='main'),
    path('outer/', views.MainView.as_view(), name='outer'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('', views.AdminView.as_view(), name='admin_admin'),
]

