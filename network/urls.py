
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("following/", views.following, name="following"),
    path("mypage/<int:user_id>/", views.userpage, name="userpage"),

    # API Routes
    path('makepost/', views.makepost, name='makepost'),
    path('getposts/<str:group>/', views.getposts, name='getposts'),
    path('mypage/<int:following_id>/follow_user/<str:changes>',
         views.follow_user, name='follow_user'),
    path("mypage/<int:following_id>/is_following/",
         views.is_following, name="isfollowing"),
    path("editpost/", views.edit_post, name="editpost")

]
