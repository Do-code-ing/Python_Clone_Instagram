from django.db import models
from django.contrib.auth.models import User


class UserImage(models.Model):
    user = models.OneToOneField(
        User, related_name="user_image", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="image", null=True, blank=True, default="profile.jpg")


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    main_image = models.ImageField(upload_to="image", null=True)
    main_comment = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} <= {self.following}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class HashTag(models.Model):
    comment = models.ManyToManyField(Comment, blank=True)
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text


class PostTag(models.Model):
    post = models.ManyToManyField(Post, blank=True)
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text
