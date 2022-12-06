from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Like
from .forms import NewPostForm, LikeUnlikeForm


def index(request):
    new_post_form = NewPostForm()
    like_unlike_form = LikeUnlikeForm()

    if request.method == "POST":
        return HttpResponseRedirect("/")

    posts = Post.objects.all().order_by("-created_time")
    posts_likes = []
    for post in posts:
        likes = Like.objects.filter(post=post.pk).count()
        posts_likes.append([post, likes])

    context = {
        "posts_likes": posts_likes,
        "new_post_form": new_post_form,
        "like_unlike_form": like_unlike_form,
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

    return


def edit_profile_view(request, user_name):
    if request.user != User.objects.get(Username = user_name):
        return
    

def follow_view(request, followee_id):
    pass


def edit_post(request, post_id):
    pass


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


def pagination(request):
    pass
