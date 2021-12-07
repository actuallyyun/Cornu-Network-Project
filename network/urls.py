
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("following/", views.following, name="following"),
    path("mypage/", views.mypage, name="mypage"),
    path("users/<int:user_id>", views.users_view, name="users"),

    # API Routes
    path('makepost/', views.makepost, name='makepost'),
    path('mypage/makepost/', views.makepost, name='makepost'),
    path('mypage/<int:following_id>/follow_user/<str:changes>',
         views.follow_user, name='follow_user'),
    path('follow_user/<int:following_id>/<str:changes>',
         views.follow_user, name='follow_user'),
    path("users/<int:following_id>/is_following/",
         views.is_following, name="isfollowing"),
    path("editpost/", views.edit_post, name="editpost"),
    path("mypage/editpost/", views.edit_post, name="editpost"),
    path('is_liking/<int:post_id>',
         views.is_liking, name='isliking'),
    path('following/is_liking/<int:post_id>',
         views.is_liking, name='isliking'),
    path('mypage/is_liking/<int:post_id>',
         views.is_liking, name='isliking'),
    path('following/like_unlike/<str:action>',
         views.like_unlike, name='likeunlike'),
    path('users/like_unlike/<str:action>',
         views.like_unlike, name='likeunlike'),
    path('like_unlike/<str:action>',
         views.like_unlike, name='likeunlike')

]
