import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts,2)
    page_number = request.GET.get('page') 
    posts = paginator.get_page(page_number)
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
    return render(request, "network/profile.html", {'username':user,'followers':followers,'following':follwing,'posts':posts, 'logged_user':request.user})


def follow(request):
    if request.method == 'GET':
        logged_user = request.GET.get('logged_user')
        user_profile = request.GET.get('user_profile')
        
        try: 
            logged_user = User.objects.get(username=logged_user)
            user_profile = User.objects.get(username=user_profile)

            if Profile.objects.filter(user=user_profile.pk, follower=logged_user.pk):
                return JsonResponse({'message':True},status=200)
            else:
                return JsonResponse({'message':False},status=200)
        except User.DoesNotExist:
            return JsonResponse({'error':'User not found'}, status=404)
    else:
        return JsonResponse({'error','GET request required'}, status=400)
    

@csrf_exempt
@login_required
def change_follow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        logged_user = data.get('logged_user')
        user_profile = data.get('user_profile')
        follow_state = data.get('follow_state')
        
        try:
            logged_user = User.objects.get(username=logged_user)
            user_profile = User.objects.get(username=user_profile)
            follow_validation = Profile.objects.filter(user=user_profile,follower=logged_user).exists()

            if  follow_state == True and follow_validation == False:
                Profile(user=user_profile,follower=logged_user).save()
                return JsonResponse({'state': True},status=200)
            
            elif follow_state == False and follow_validation == True:
                state_to_change = Profile.objects.get(user=user_profile,follower=logged_user)
                state_to_change.delete()
                return JsonResponse({'state':False},status=200)

        except User.DoesNotExist:
            return JsonResponse({'error':'User not found'},status=404)
    else:
        return JsonResponse({'error','PUT request required'}, status=400)


def following(request):
    if request.user.is_authenticated:
        following_users = []
        following_profiles = Profile.objects.filter(follower=request.user.pk)

        for following_profile in following_profiles:
            following_users.append(following_profile.user)

        posts = Post.objects.filter(user__in=following_users).order_by('-date')
        return render(request,'network/following.html',{'posts':posts})
    else:
        return HttpResponseRedirect(reverse('login'))