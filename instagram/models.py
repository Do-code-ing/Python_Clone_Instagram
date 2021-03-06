from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        upload_to="image", null=True, blank=True, default="profile.jpg")
    name = models.CharField(max_length=50, blank=True)
    website = models.CharField(max_length=200, blank=True)
    introduction = models.TextField(blank=True)
    gender = models.CharField(max_length=20, default="conceal")
    custom_gender = models.CharField(max_length=12, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    main_image = models.ImageField(upload_to="image", null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    @property
    def create_date_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days) + '일 전'
        elif time < timedelta(days=365):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days // 7) + '주'
        else:
            return f"{self.create_date.year}년 {self.create_date.month}월 {self.create_date.day}일"


class PostComment(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @property
    def create_date_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days) + '일 전'
        elif time < timedelta(days=365):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days // 7) + '주'
        else:
            return f"{self.create_date.year}년 {self.create_date.month}월 {self.create_date.day}일"


class PostTag(models.Model):
    post = models.ManyToManyField(Post, blank=True)
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text


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

    @property
    def create_date_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days) + '일 전'
        elif time < timedelta(days=365):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days // 7) + '주'
        else:
            return f"{self.create_date.year}년 {self.create_date.month}월 {self.create_date.day}일"


class HashTag(models.Model):
    comment = models.ManyToManyField(Comment, blank=True)
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text


class Notice(models.Model):
    TYPE_CHOICES = (
        ("like", "like"),
        ("comment", "comment"),
        ("follow", "follow"),
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    check = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    @property
    def create_date_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days) + '일 전'
        elif time < timedelta(days=365):
            time = datetime.now(tz=timezone.utc).date() - \
                self.create_date.date()
            return str(time.days // 7) + '주'
        else:
            return f"{self.create_date.year}년 {self.create_date.month}월 {self.create_date.day}일"
