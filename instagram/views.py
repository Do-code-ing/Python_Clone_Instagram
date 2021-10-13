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
            main_image=request.FILES.get('main_image'),
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
    post = post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()
    return redirect("instagram:index")


@login_required
def search(request):
    if request.method == "POST":
        search_for = request.POST['search_for']
        user_list = User.objects.filter(username__icontains=search_for)
        post_list = Post.objects.filter(title__icontains=search_for)
        context = {
            "search_for": search_for,
            "user_list": user_list,
            "post_list": post_list,
        }
        return render(request, "instagram/search.html", context)
    else:
        return render(request, "instagram/search.html")


def user_detail(request, username):
    user_ = get_object_or_404(User, username=username)
    context = {
        "user_": user_
    }
    return render(request, "instagram/user_detail.html", context)


@login_required
def like(request, pk):
    post = get_object_or_404(Post, id=pk)
    try:
        liked = Like.objects.get(user=request.user, post=post)
        liked.delete()
    except:
        Like.objects.create(user=request.user, post=post)
    finally:
        return redirect("instagram:post_detail", pk=pk)


@login_required
def follow(request, username):
    follower = get_object_or_404(User, username=username)
    following = get_object_or_404(User, username=request.user.username)
    if follower == following:   # 404 발생시키자
        return redirect("instagram:index")
    try:
        followed = Follow.objects.get(
            follower=follower, following=following)
        followed.delete()
    except:
        Follow.objects.create(follower=follower, following=following)
    finally:
        return redirect("instagram:user_detail", username=username)
