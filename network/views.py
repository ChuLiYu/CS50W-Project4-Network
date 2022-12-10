from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Post, Like, Following
from .forms import EditPostForm, NewPostForm, LikeUnlikeForm, FollowForm


def index(request):
    new_post_form = NewPostForm()
    like_unlike_form = LikeUnlikeForm()
    edit_post_form = EditPostForm()

    if request.method == "POST":
        return HttpResponseRedirect("/")

    posts = Post.objects.all().order_by("-created_time")
    posts_likes = []
    for post in posts:
        likes = Like.objects.filter(post=post.pk).count()
        posts_likes.append([post, likes])

    # pagenate
    limit = 10
    paginator = Paginator(posts_likes, limit)
    page = request.GET.get("page")
    try:
        posts_likes = paginator.page(page)
    except PageNotAnInteger:
        posts_likes = paginator.page(1)
    except EmptyPage:
        posts_likes = paginator.page(paginator.num_pages)

    context = {
        "posts_likes": posts_likes,
        "new_post_form": new_post_form,
        "like_unlike_form": like_unlike_form,
        "edit_post_form": edit_post_form,
    }

    return render(request, "network/index.html", context)


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post_view(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            print("in valid")
            revised_form = form.save(commit=False)
            revised_form.creator = request.user

            revised_form.save()
            return HttpResponseRedirect("/")
    else:
        pass
    context = {"new_post_form": NewPostForm()}
    return render(request, "network/new.html", context)


def profile_view(request, user_name):
    like_unlike_form = LikeUnlikeForm()
    follow_form = FollowForm()
    # For (un)like and follow
    if request.method == "POST":
        return HttpResponseRedirect("/")

    # user's posts
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(creator=user).order_by("-created_time")

    # apped post and it liks numbers
    posts_likes = []
    for post in posts:
        likes = Like.objects.filter(post=post.pk).count()
        posts_likes.append([post, likes])

    # count user's follower and followee
    follower_number = Following.objects.filter(follower=user).count()
    followee_number = Following.objects.filter(followee=user).count()
    print(f"Follower number: {follower_number}, Followee number: {followee_number}")
    context = {
        "posts_likes": posts_likes,
        "like_unlike_form": like_unlike_form,
        "follow_form": follow_form,
        "user_name": user_name,
        "follower_number": follower_number,
        "followee_number": followee_number,
    }

    return render(request, "network/profile.html", context)


def edit_profile_view(request, user_name):
    if request.user != User.objects.get(Username=user_name):
        return


def follow_undo_view(request, followee_user_name):
    follower = request.user
    followee = User.objects.get(username=followee_user_name)
    follow_realation = Following.objects.filter(follower=follower, followee=followee)
    if followee == follower:
        return HttpResponseRedirect(f"/profile/{followee_user_name}")
    if request.method == "GET":
        return HttpResponseRedirect(f"/profile/{followee_user_name}")

    form = FollowForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(f"/profile/{followee_user_name}")

    if follow_realation:
        follow_realation.delete()
    else:
        temp = form.save(commit=False)
        temp.follower = follower
        temp.followee = User.objects.get(username=followee_user_name)
        temp.save()

    return HttpResponseRedirect(f"/profile/{followee_user_name}")


@login_required
def edit_post_view(request, post_id):
    if request.method != "POST":
        return HttpResponseRedirect("/")
    user = User.objects.get(username=request.user)
    post = Post.objects.filter(pk=post_id, creator=user)
    if not post:
        return HttpResponseRedirect("/")
    # save new context to db
    post.update(context=request.POST.get("context"))
    return HttpResponseRedirect("/")


@login_required
def like_unlike_view(request, post_id):
    if request.method == "GET":
        return
    post = Post.objects.get(pk=post_id)
    like = Like.objects.filter(post=post, creator=request.user)

    # Like and Unlike based on like sql is exist or not
    if like:
        form = LikeUnlikeForm(request.POST, instance=like.first())
        if form.is_valid():
            like.delete()
    else:
        form = LikeUnlikeForm(request.POST)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.creator = request.user
            post = Post.objects.get(pk=post_id)
            temp_form.post = post
            temp_form.save()
    return HttpResponseRedirect("/")





# Show only sign in user for their following users' posts
@login_required
def following_view(request):
    new_post_form = NewPostForm()
    like_unlike_form = LikeUnlikeForm()

    if request.method == "POST":
        return HttpResponseRedirect("/")

    # For filter out followed user's post
    user = User.objects.get(username=request.user)
    followees = (
        Following.objects.filter(follower=user)
        .values_list("followee", flat=True)  # get followee col
        .distinct()
    )
    posts = Post.objects.filter(creator__in=followees).order_by("-created_time")

    posts_likes = []
    for post in posts:
        likes = Like.objects.filter(post=post.pk).count()
        posts_likes.append([post, likes])

    # Pagination
    limit = 10
    paginator = Paginator(posts_likes, limit)
    page = request.GET.get("page")
    try:
        posts_likes = paginator.page(page)
    except PageNotAnInteger:
        posts_likes = paginator.page(1)
    except EmptyPage:
        posts_likes = paginator.page(paginator.num_pages)

    context = {
        "posts_likes": posts_likes,
        "new_post_form": new_post_form,
        "like_unlike_form": like_unlike_form,
    }

    return render(request, "network/index.html", context)
