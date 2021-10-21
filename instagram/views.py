from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from .models import *
from .forms import *
from collections import deque


def text_to_hashtag(texts):
    texts = texts.split("\r\n")
    tags = []
    comments = []

    for text in texts:
        tagging = False
        temp = []
        q = deque(text)
        while q:
            x = q.popleft()

            if x == "#":
                if tagging:
                    comments.append(temp)
                temp = ["#"]
                tagging = True
            elif x == " ":
                if tagging and len(temp) > 1:
                    tags.append(temp)
                else:
                    temp.append(x)
                    comments.append(temp)
                temp = []
                tagging = False
            else:
                temp.append(x)

        if temp:
            if temp[0] == "#" and len(temp) > 1:
                tags.append(temp)
            else:
                comments.append(temp)

        if comments[-1] != ["\n"]:
            comments.append(["\n"])

    return tags, comments


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            author=request.user).order_by("-create_date")

        for following in request.user.following.all():
            posts |= Post.objects.filter(
                author=following.follower).order_by("-create_date")

        context = {
            "posts": posts,
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

        return redirect("instagram:update", pk=post.pk)

    context = {
        "post_form": PostForm,
        "image_form": ImageForm,
    }
    return render(request, "instagram/post.html", context)


def update(request, pk):
    post = get_object_or_404(Post, id=pk)
    try:
        images = Image.objects.filter(post=post)
    except:
        images = None

    if request.user == post.author:
        if request.method == "POST":
            for tag in post.posttag_set.all():
                tag.post.remove(post)

            text = request.POST["main_comment"]
            tags, comments = text_to_hashtag(text)
            result = []
            print(comments)
            print(tags)
            for comment in comments:
                if comment:
                    result.append("".join(comment))

            post.main_comment = "".join(result)
            for tag in tags:
                tag = "".join(tag)
                try:
                    tag = PostTag.objects.get(text=tag)
                except:
                    tag = PostTag.objects.create(text=tag)
                finally:
                    tag.post.add(post)

            post.save()
            return redirect("instagram:index")
        else:
            context = {
                "post_comment_form": PostCommentForm(instance=post),
                "post": post
            }
            if images is not None:
                context["images"] = images
            return render(request, "instagram/update.html", context)
    else:
        return redirect("instagram:index")  # 에러 발생


def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()
        return redirect("instagram:index")
    else:
        return redirect("instagram:index")  # 에러 발생


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post.id)
    context = {
        "post": post,
        "comments": comments,
        "comment_form": CommentForm,
    }

    try:
        liked = post.like_set.get(user=request.user)
    except:
        liked = None

    if liked:
        context["liked"] = True

    try:
        Follow.objects.get(follower=post.author, following=request.user)
        followed = "True"
    except:
        followed = "False"

    context["followed"] = followed

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

            follow_result = []
            for user_ in user_result:
                try:
                    Follow.objects.get(follower=user_, following=request.user)
                    follow_result.append(user_)
                except:
                    continue

            context["follow_result"] = follow_result
            context["user_result"] = user_result
            context["target"] = "both"

        return render(request, "instagram/search.html", context)
    else:
        return render(request, "instagram/search.html")


def profile(request, username):
    user_ = get_object_or_404(User, username=username)
    try:
        Follow.objects.get(follower=user_, following=request.user)
        followed = "True"
    except:
        followed = "False"

    context = {
        "user_": user_,
        "followed": followed,
    }
    return render(request, "instagram/profile.html", context)


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
        return redirect("instagram:profile", username=username)


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
