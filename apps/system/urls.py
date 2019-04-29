from django.urls import path
from system import views

urlpatterns = [
    path('position/add/', views.PositionAddView.as_view(), name="position_add"),
    path('position/rights/', views.PositionAjax.as_view(), name="rights"),
    path("position/", views.PositionView.as_view(), name="position"),
]