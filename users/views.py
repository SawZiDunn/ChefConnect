from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, logout, authenticate

from recipe.models import Recipe
from .forms import LoginForm, RegisterForm
from .models import CustomUser


def profile(request):
    profile_user = CustomUser.objects.get(pk=request.user.id)  # request.user
    recipes = profile_user.created_recipes.all()
    return render(request, 'users/profile.html', {"profile_user": profile_user, "recipes": recipes})


def chef_profile(request, chef_id: int):
    profile_user = CustomUser.objects.get(id=chef_id)

    # recipes = Recipe.objects.filter(chef_id=chef_id)
    recipes = profile_user.created_recipes.all()
    if request.user.id == chef_id:
        return redirect('users:profile')
    return render(request, 'users/profile.html', {"profile_user": profile_user, "recipes": recipes})


def edit_profile(request):
    pass


def login_view(request):
    if request.method == "POST":

        form = LoginForm(data=request.POST)
        print(request.POST)
        print(form.is_valid())

        user = authenticate(username='john', password='john_password')
        print(user)

        if form.is_valid():
            user = form.get_user()

            login(request, user)
            return redirect("recipe:index")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # save user to db
            return redirect("users:login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")
