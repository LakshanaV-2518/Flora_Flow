from django.urls import path, include
from . import views
from .views import authView
from .views import post_delete
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
app_name = "blog"

class LogoutView(LogoutView):
    next_page ='login'

urlpatterns = [
    # Blog-related URLs
    path("post/", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:id>/update/", views.post_update, name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:pk>/view", views.post_view, name="post_view"),
    path("logout/",auth_views.LogoutView.as_view(),name='logout'),
    # User-related and other URLs
    path("home/", views.home, name="home"),
    path("signup/", authView, name="authView"),
    path("", include("django.contrib.auth.urls")),
    path("home/care-tips/", views.care_tips, name="care_tips"),
]
