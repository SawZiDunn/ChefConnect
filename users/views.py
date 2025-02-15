from django.shortcuts import render
from django.http import HttpRequest

app_name = 'users'
# Create your views here.


def index(request):
    return render(request, "users/index.html")


def login(request):
    return render(request, "users/login.html")


def register(request):
    return render(request, "users/register.html")

