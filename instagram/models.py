from django.db import models
from django.db.models.deletion import CASCADE


class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Image(models.Model):
    Post = models.ForeignKey(Post, on_delete=CASCADE)
