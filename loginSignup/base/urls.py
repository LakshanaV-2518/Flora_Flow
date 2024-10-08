from django.urls import path, include
from . import views
from .views import authView
from .views import post_delete
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = "blog"


urlpatterns = [
    # User-related and other URLs
    
    path("", authView, name="authView"),
    path("", include("django.contrib.auth.urls")),
    path("home/", views.home, name="home"),
    path("home/care-tips/", views.care_tips, name="care_tips"),
    
    # Blog-related URLs
    path("post/", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:id>/update/", views.post_update, name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:id>/view", views.post_view, name="post_view"),
]