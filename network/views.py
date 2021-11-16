import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.deletion import SET_DEFAULT
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import PostLiking, User, UserFollowing, Post
from django.core.paginator import Paginator


def index(request):

    # Authenticated users view the posts
    if request.user.is_authenticated:
        # Display all existing posts
        posts = Post.objects.order_by(
            "-date_time_created").all()
        p = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj

        })
    # Everyone else is prompt to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def makepost(request):

    # API view Posting must be via POST method
    if request.method != "POST":
        return JsonResponse({"error": "POST request required",
                             'ok': False}, status=200)
    else:
        # Get contents and make the post
        data = json.loads(request.body)
        content = data.get("content", "")

        post = Post(poster=request.user, content=content)
        post.save()

        return JsonResponse({"message": "Post successfully.", "ok": True}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def following(request):
    # This page displays posts from users that this user is following at the moment
    posts = request.user.posts_followed_user()
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@login_required
def mypage(request):
    # This page displays all the posts from this user herself
    my_posts = Post.objects.filter(poster=request.user)
    p = Paginator(my_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/mypage.html", {
        "page_obj": page_obj,
        "num_follows": request.user.num_follows(),
        "num_followers": request.user.num_followers()
    })


@login_required
def users_view(request, user_id):
    # This view renders the page of a user
    my_posts = Post.objects.filter(poster=user_id)
    p = Paginator(my_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/userpage.html", {
        "page_obj": page_obj,
        "num_follows": User.objects.get(pk=user_id).num_follows(),
        "num_followers": User.objects.get(pk=user_id).num_followers(),
        "user_id": user_id
    })


@csrf_exempt
@login_required
def follow_user(request, following_id, changes):
    # API view Recieved Json data and process it. Create or delete userfollowing object accordingly
    if request.method != "PUT":
        return JsonResponse({
            "error": "PUT request required", 'ok': False}, status=400)
    else:

        if changes == "follow":
            follow_user = UserFollowing(
                user=request.user, following_user=User.objects.get(id=following_id))

            follow_user.save()

            return JsonResponse({"message": "Followed successfully", "ok": True}, status=201)

        elif changes == "unfollow":
            unfollow_user = UserFollowing.objects.get(
                user=request.user, following_user_id=following_id)
            unfollow_user.delete()
            return JsonResponse({"message": "Unfollowed successfully", "ok": True}, status=201)

        else:
            return JsonResponse({
                "error": "Unkown command", 'ok': False}, status=400)


@login_required
def is_following(request, following_id):
    # API view This function recieves Json data and check if the current user is following the following_id user
    # It returns True if it is, Flase if not
    if UserFollowing.objects.filter(user=request.user, following_user_id=following_id).exists():
        return JsonResponse({"isFollowing": True}, status=201)
    else:
        return JsonResponse({"isFollowing": False}, status=201)


def edit_post(request):
    # API view This function handles the edit post request.

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required",
                            'ok': False}, status=400)
    else:
        # Get contents
        data = json.loads(request.body)
        content = data.get("content", "")
        post_id = data.get("post_id", "")
        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()

        return JsonResponse({"message": "Edit post successfully.", "ok": True}, status=201)


@csrf_exempt
def like_unlike(request, action):
    # This API handles like and unlike request through an PUT request
    if request.method == "PUT":
        # get the data
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        post = Post.objects.get(pk=post_id)

        if action == "like":
            # Create a PostLiking instance, need post id and user id
            post_liking = PostLiking.objects.create(
                user=request.user, post=post)
            post_liking.save()
            return JsonResponse({"message": "Liked successfully", "ok": True}, status=201)
        elif action == "unlike":
            # Find the PostLiking instance and delete it from the database
            post_unlike = PostLiking.objects.filter(
                user=request.user, post=post)
            post_unlike.delete()
            return JsonResponse({"message": "Unliked successfully", "ok": True}, status=201)
        else:
            return JsonResponse({"error": "Unkown action.",
                                 'ok': False}, status=400)

    else:
        return JsonResponse({"error": "PUT request required",
                            'ok': False}, status=400)


def is_liking(request, post_id):
    # This API checks if the current user already liked the post or not
    if PostLiking.objects.filter(user=request.user, post=post_id).exists():
        return JsonResponse({"isLiking": True}, status=201)
    else:
        return JsonResponse({"isLiking": False}, status=200)
