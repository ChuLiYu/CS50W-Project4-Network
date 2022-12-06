from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post_view, name="new_post_path"),
    path("like/<int:post_id>", views.like_unlike_view, name="like_unlike_path"),
    path("profile/<str:user_name>", views.profile_view, name="profile_path"),
]
