from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<str:username>", views.profile, name='profile'),
    path('following', views.following, name='following'),

    # Apis
    path("follow", views.follow, name='follow'),
    path("change_follow",views.change_follow,name='change_follow'),
    path("edit",views.edit,name='edit'),
    path("like",views.like,name="like")
]
