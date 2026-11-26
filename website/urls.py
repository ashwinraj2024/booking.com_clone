from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stays/", views.stays, name="stays"),
    path("stays/<int:hotel_id>/", views.hotel_detail, name="hotel_detail"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
]
