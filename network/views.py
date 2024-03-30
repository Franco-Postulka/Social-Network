from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, "network/index.html",{'posts':posts})


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
    

def post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST['text']
            post = Post(user=request.user, text=text)
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))
    

def profile(request, username):
    user = User.objects.get(username=username)
    follwing = Profile.objects.filter(follower=user.pk).count()
    followers = Profile.objects.filter(user=user.pk).count()
    posts = Post.objects.filter(user=user).order_by('-date')
    return render(request, "network/profile.html", {'username':user,'followers':followers,'following':follwing,'posts':posts})