from django.urls import path
from . import views

app_name = "instagram"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/", views.post, name="post"),
    path("update/<int:pk>/", views.update, name="update"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("post_detail/<int:pk>/", views.post_detail, name="post_detail"),
    path("post_detail/<int:pk>/like/", views.like, name="like"),
    path("search/", views.search, name="search"),
    path("user_detail/<str:username>/", views.user_detail, name="user_detail"),
    path("user_detail/<str:username>/follow/", views.follow, name="follow")
]
