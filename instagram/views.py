from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            author=request.user).order_by("-create_date")

        for following in request.user.following.all():
            posts |= Post.objects.filter(
                author=following.follower).order_by("-create_date")

        context = {
            "posts": posts,
            "page_name": "index",
        }

        return render(request, "instagram/index.html", context)
    return redirect("registration:login")


@login_required
def post(request):
    if request.method == "POST":
        post = Post.objects.create(
            author=request.user,
            main_image=request.FILES.get('main_image'),
        )
        images = request.FILES.getlist('image')
        for image in images:
            Image.objects.create(post=post, image=image)

        text = request.POST["text"]
        comment = Comment.objects.create(
            author=request.user, post=post, text=text)
        tagging = False
        tag = ""
        for t in text:
            if t == "#":
                if tagging:
                    tag = ""
                tagging = True
            elif t == " ":
                tagging = False
                try:
                    hashtag = HashTag.objects.get(text=tag)
                except:
                    hashtag = HashTag.objects.create(text=tag)
                finally:
                    hashtag.comment.add(comment)
                tag = ""
            if tagging:
                tag += t

        if tag.startswith("#"):
            try:
                hashtag = HashTag.objects.get(text=tag)
            except:
                hashtag = HashTag.objects.create(text=tag)
            finally:
                hashtag.comment.add(comment)

        return redirect("instagram:index")

    context = {
        "post_form": PostForm,
        "image_form": ImageForm,
        "comment_form": PostingCommentForm,
        "page_name": "profile",
    }
    return render(request, "instagram/post.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post.id)
    context = {
        "post": post,
        "comments": comments,
        "comment_form": CommentForm,
    }
    return render(request, "instagram/post_detail.html", context)


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        Comment.objects.create(
            author=request.user,
            post=post,
            text=request.POST["text"]
        )
    return redirect("instagram:post_detail", pk=pk)


@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, id=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect("instagram:post_detail", pk=pk)


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
                "page_name": "profile",
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


def search(request):
    if request.method == "POST":
        search_for = request.POST['search_for']
        target = "tag only"
        context = {
            "search_for": search_for,
            "target": target,
        }

        post_ids = []
        hashtags = HashTag.objects.filter(text__icontains=search_for)
        for tag in hashtags:
            for comment in tag.comment.all():
                post_ids.append(comment.post.pk)

        tag_result = Post.objects.filter(id__in=post_ids)
        tag_result_like = tag_result.order_by("-like")[:6]
        tag_result_date = tag_result.order_by("-create_date")
        context["tag_result_like"] = tag_result_like
        context["tag_result_date"] = tag_result_date

        if not search_for.startswith("#"):
            user_result = User.objects.filter(username__icontains=search_for)
            user_result = user_result.annotate(
                count=Count("follower")).order_by("-count")
            context["user_result"] = user_result
            context["target"] = "both"

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
def follow(request, username):
    follower = get_object_or_404(User, username=username)
    following = get_object_or_404(User, username=request.user.username)
    if follower == following:   # 404 발생시키자
        messages.error(request, "자기 자신을 팔로우 할 수 없습니다.")
        return redirect("instagram:index")
    try:
        followed = Follow.objects.get(
            follower=follower, following=following)
        followed.delete()
    except:
        Follow.objects.create(follower=follower, following=following)
    finally:
        return redirect("instagram:user_detail", username=username)


@login_required
def dm(request):
    return render(request, "instagram/dm.html")


@login_required
def notice(request):
    return render(request, "instagram/notice.html")


@login_required
def profile_edit(request):
    try:
        user_image = UserImage.objects.get(user=request.user)
    except:
        user_image = UserImage.objects.create(user=request.user)

    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            user_image.image = image
            user_image.save()

    context = {
        "user_image_form": UserImageForm,
    }
    return render(request, "instagram/profile_edit.html", context)


@login_required
def change_profile_image(request):
    try:
        user_image = UserImage.objects.get(user=request.user)
    except:
        user_image = UserImage.objects.create(user=request.user)
    user_image.image = "profile.jpg"
    user_image.save()
    return redirect("instagram:profile_edit")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 자동 재로그인
            messages.success(request, "비밀번호 변경이 완료됐습니다.")
        else:
            messages.error(request, "기존 비밀번호와 새 비밀번호를 다시 확인해주세요.")

    form = PasswordChangeForm(request.user)
    return render(request, "instagram/change_password.html", {"form": form})
