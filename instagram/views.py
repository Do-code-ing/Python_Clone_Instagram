from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from instagram.models import *


def index(request):
    if request.user.is_authenticated:
        return render(request, "instagram/index.html")
    return redirect(reverse("registration:login"))


def post(request):
    if request.method == "POST":
        post = Post.objects.create(
            title=request.POST["title"],
            author=request.user,
            content=request.POST["content"],
        )
        images = request.FILES.getlist('images')
        print(images)
        for image in images:
            Image.objects.create(post=post, image=image)
        return redirect(reverse("instagram:index"))
    return render(request, "instagram/post.html")
