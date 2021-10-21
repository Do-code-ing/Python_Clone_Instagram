from django.urls import path
from . import views

app_name = "instagram"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/", views.post, name="post"),
    path("update/<pk>/", views.update, name="update"),
    path("delete/<pk>/", views.delete, name="delete"),
    path("post_detail/<pk>/", views.post_detail, name="post_detail"),
    path("post_detail/<pk>/comment_create",
         views.comment_create, name="comment_create"),
    path("post_detail/<pk>/comment_delete/<comment_pk>/",
         views.comment_delete, name="comment_delete"),
    path("post_detail/<pk>/like/", views.like, name="like"),
    path("search/<search_for>", views.search, name="search"),
    path("profile/<username>/", views.profile, name="profile"),
    path("profile/<username>/follow/", views.follow, name="follow"),
    path("dm/", views.dm, name="dm"),
    path("notice/", views.notice, name="notice"),
    path("profile_edit/", views.profile_edit, name="profile_edit"),
    path("profile_edit/reset_profile_image",
         views.reset_profile_image, name="reset_profile_image"),
    path("change_password/", views.change_password, name="change_password"),
]
