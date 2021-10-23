from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from instagram.models import *


def signup(request):
    if request.user.is_authenticated:
        auth.logout(request)

    if request.method == "POST":
        try:
            User.objects.get(username=request.POST["username"])
            messages.error(request, "이미 존재하는 아이디입니다.")
            return render(request, "registration/signup.html")
        except:
            if request.POST["password1"] == request.POST["password2"]:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST["email"],
                )
                Profile.objects.create(user=user, name=user.username)
                auth.login(request, user)
                return redirect("instagram:index")
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return render(request, "registration/signup.html")
    return render(request, "registration/signup.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("instagram:index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("instagram:index")
        messages.error(request, "아이디 혹은 비밀번호가 틀렸습니다.")
        return render(request, "registration/login.html")
    return render(request, "registration/login.html")


def logout(request):
    auth.logout(request)
    return redirect("registration:login")


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        password = request.POST["password"]
        if check_password(password, user.password):
            user.delete()
            return redirect("registration:login")

    return render(request, "registration/delete_account.html")
