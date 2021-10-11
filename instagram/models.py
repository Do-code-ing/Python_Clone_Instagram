from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Image(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
