from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, LoginForm


def login_view(request):

    if request.method == "POST":

        form = LoginForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("recipe:index")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("home")  # Change "home" to your desired redirect
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


