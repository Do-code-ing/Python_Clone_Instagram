from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        return render(request, "instagram/index.html")
    return redirect("registration:login")


@login_required
def post(request):
    if request.method == "POST":
        post = Post.objects.create(
            title=request.POST["title"],
            author=request.user,
            content=request.POST["content"],
        )
        images = request.FILES.getlist('image')
        for image in images:
            Image.objects.create(post=post, image=image)
        return redirect("instagram:index")
    context = {
        "post_form": PostForm,
        "image_form": ImageForm,
    }
    return render(request, "instagram/post.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    context = {
        "post": post,
    }
    return render(request, "instagram/post_detail.html", context)


def update(request, pk):
    post = get_object_or_404(Post, id=pk)
    images = None
    try:
        images = Image.objects.filter(post=post)
    except:
        pass

    if request.user == post.author:
        if request.method == "POST":
            post.title = request.POST["title"]
            post.content = request.POST["content"]
            post.save()
            return redirect("instagram:index")
        else:
            context = {
                "post_form": PostForm(instance=post),
            }
            if images is not None:
                context["images"] = images
            return render(request, "instagram/update.html", context)
    else:
        return redirect("instagram:index")


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect("instagram:index")
