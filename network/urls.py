
from django.urls import path
# from django.conf.urls import url
from django.urls import re_path
from . import views

# app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/config/<str:username>", views.config, name="config"),
    path("profile/<str:username>/newpost", views.newpost, name="newpost"),
    path("<str:post_id>/delete", views.delete, name="delete"),
    path("following/<str:username>", views.following, name='following'),
    path("posts/<int:post_id>/edit", views.edit, name="edit"),
    path("post-comment/<str:action>", views.newComment, name="post-comment"),
    re_path(r'^likepost/$', views.like_post, name='like-post')
]
