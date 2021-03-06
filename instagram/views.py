from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from .models import *
from .forms import *
from collections import deque


def text_to_hashtag(texts):
    texts = texts.lower()
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

        if comments and comments[-1] != ["\n"]:
            comments.append(["\n"])

    return tags, comments


@login_required
def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)

        followers = []
        for following in request.user.following.all():
            posts |= Post.objects.filter(author=following.follower)
            followers.append(following.follower)

        posts |= Post.objects.filter(author__in=followers)

        followers = User.objects.filter(
            username__in=followers).order_by("-last_login")[:7]

        context = {
            "posts": posts,
            "followers": followers,
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


@login_required
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

            text = request.POST["text"]
            tags, comments = text_to_hashtag(text)
            result = []

            for comment in comments:
                if comment:
                    result.append("".join(comment))

            comment = "".join(result)

            try:
                post_comment = PostComment.objects.get(post=post)
                post_comment.text = comment
                post_comment.save()
            except:
                post_comment = PostComment.objects.create(
                    post=post, text=comment)

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
                "post": post
            }
            try:
                context["post_comment_form"] = PostCommentForm(
                    instance=post.postcomment)
            except:
                context["post_comment_form"] = PostCommentForm

            if images is not None:
                context["images"] = images
            return render(request, "instagram/update.html", context)
    else:
        return redirect("instagram:index")  # ?????? ??????


@login_required
def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()
        return redirect("instagram:index")
    else:
        return redirect("instagram:index")  # ?????? ??????


@login_required
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
        text = request.POST["text"]
        tags, comments = text_to_hashtag(text)
        result = []

        for comment in comments:
            if comment:
                result.append("".join(comment))

        result = "".join(result)
        comment = Comment.objects.create(
            author=request.user, post=post, text=result)

        for tag in tags:
            tag = "".join(tag)
            try:
                tag = HashTag.objects.get(text=tag)
            except:
                tag = HashTag.objects.create(text=tag)
            finally:
                tag.comment.add(comment)

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


@login_required
def search(request, search_for):
    target = "tag only"
    context = {
        "search_for": search_for,
        "target": target,
    }

    if not search_for.startswith("#"):
        user_result = User.objects.filter(username__icontains=search_for)
        user_result |= User.objects.filter(profile__name__icontains=search_for)
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

        search_for = "#" + search_for

    post_ids = set()
    hashtags = HashTag.objects.filter(text__iexact=search_for)
    for tag in hashtags:
        for comment in tag.comment.all():
            post_ids.add(comment.post.pk)

    tag_result = Post.objects.filter(id__in=post_ids)

    posttags = PostTag.objects.filter(text__iexact=search_for)
    for tag in posttags:
        tag_result |= tag.post.all()

    tag_result_like = tag_result.order_by("-like", "-create_date")[:6]
    tag_result_date = tag_result.order_by("-create_date")
    context["tag_result_like"] = tag_result_like
    context["tag_result_date"] = tag_result_date

    return render(request, "instagram/search.html", context)


@login_required
def profile(request, username):
    user_ = get_object_or_404(User, username=username)
    following_with_my_following = []
    if request.user != user_:
        for following in request.user.following.all():
            my_following = following.follower
            check = Follow.objects.filter(
                follower=user_, following=my_following)
            if check:
                following_with_my_following.append(my_following)

    try:
        Follow.objects.get(follower=user_, following=request.user)
        followed = "True"
    except:
        followed = "False"

    context = {
        "user_": user_,
        "followed": followed,
        "follow_list": following_with_my_following,
    }
    return render(request, "instagram/profile.html", context)


@login_required
def follow(request, username):
    follower = get_object_or_404(User, username=username)
    following = get_object_or_404(User, username=request.user.username)
    if follower == following:   # 404 ???????????????
        messages.error(request, "?????? ????????? ????????? ??? ??? ????????????.")
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
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if "image_change" in request.POST:
            image = request.FILES.get('user_image')
            if image:
                profile.user_image = image
                profile.save()
        else:
            name = request.POST["name"]
            website = request.POST["website"]
            introduction = request.POST["introduction"]
            gender = request.POST["gender"]
            profile.name = name
            profile.website = website
            profile.introduction = introduction

            if gender not in ("male", "female", "conceal"):
                profile.gender = "custom"
                profile.custom_gender = gender
            else:
                profile.gender = gender
                profile.custom_gender = ""

            profile.save()

    context = {
        "user_image_form": UserImageForm,
        "profile_form": ProfileForm(instance=profile),
    }
    return render(request, "instagram/profile_edit.html", context)


@login_required
def reset_profile_image(request):
    profile = Profile.objects.get(user=request.user)
    profile.user_image = "profile.jpg"
    profile.save()
    return redirect("instagram:profile_edit")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ?????? ????????????
            messages.success(request, "???????????? ????????? ??????????????????.")
        else:
            messages.error(request, "?????? ??????????????? ??? ??????????????? ?????? ??????????????????.")

    form = PasswordChangeForm(request.user)
    return render(request, "instagram/change_password.html", {"form": form})
