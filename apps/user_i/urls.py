from django.urls import path
from user_i import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path("", cache_page(60*10)(views.UserView.as_view()), name="user_i"),
    path("", views.UserView.as_view(), name="user_i"),

]