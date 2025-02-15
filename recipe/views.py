from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate


def index(request):
    return render(request, "recipe/index.html")

def new(request):
    return render(request, "recipe/new.html")


