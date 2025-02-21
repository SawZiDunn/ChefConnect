from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from interactions.models import Follow
from .forms import LoginForm, RegisterForm, ProfileEditForm, CustomPasswordChangeForm
from .models import CustomUser


@login_required
def profile(request):
    profile_user = CustomUser.objects.get(pk=request.user.id)  # request.user
    recipes = profile_user.created_recipes.all()

    return render(request, 'users/profile.html',
                  {"profile_user": profile_user, "recipes": recipes, "recipe_count": len(recipes),
                   "follower_count": profile_user.followers.count(),
                   "following_count": profile_user.followings.count()})


@login_required
def chef_profile(request, chef_id: int):
    profile_user = CustomUser.objects.get(id=chef_id)

    # print(profile_user.followers.all())
    is_following = Follow.objects.filter(follower=request.user,
                                         followed_user=profile_user).exists()  # checks if the current user follows profile user

    print(is_following)

    # recipes = Recipe.objects.filter(chef_id=chef_id)
    recipes = profile_user.created_recipes.all()

    if request.user.id == chef_id:
        return redirect('users:profile')

    return render(request, 'users/profile.html',
                  {"profile_user": profile_user, "recipes": recipes, "is_following": is_following,
                   "recipe_count": len(recipes), "follower_count": profile_user.followers.count(),
                   "following_count": profile_user.followings.count()})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                # Save the user first
                user = form.save()

                # Immediately update the session
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('users:profile')
            except Exception as e:
                # If something goes wrong, log it and revert
                print(f"Error during password change: {e}")  # For debugging
                messages.error(request, 'An error occurred while changing your password. Please try again.')
                return redirect('users:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {
        'form': form
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')  # Redirect to profile page
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {
        'form': form
    })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)  # Add request parameter

        print("Login attempt:")
        print(f"Username: {request.POST.get('username')}")
        print(f"Password: {request.POST.get('password')}")

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            print("Authenticated user: ", user)

            if user is not None:
                login(request, user)
                print(f"Login successful for user: {username}")
                return redirect("recipe:index")
            else:
                print(f"Authentication failed for user: {username}")
        else:
            print("Form errors:", form.errors)
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        print("Form data:", request.POST)
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)

        if form.is_valid():
            user = form.save()

            print(f"User created: {user.username}")
            print(f"User password hash: {user.password}")  # Check if password is hashed

            # Test immediate authentication
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            print("username:", username, "password:", password)
            test_user = authenticate(username=username, password=password)
            print(f"Test authentication after registration: {test_user}")

            if test_user is None:
                # Try to get the user from the database
                from django.contrib.auth import get_user_model
                User = get_user_model()
                db_user = User.objects.filter(username=username).first()
                print(f"User in database: {db_user}")
                if db_user:
                    print(f"DB user password hash: {db_user.password}")

            return redirect("users:login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")
