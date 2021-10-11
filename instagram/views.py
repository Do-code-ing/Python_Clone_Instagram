from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


def index(request):
    if request.user.is_authenticated:
        return render(request, "instagram/index.html")
    return redirect(reverse("registration:login"))
