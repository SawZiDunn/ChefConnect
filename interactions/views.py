from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Like, Review, Follow
from recipe.models import Recipe
from users.models import CustomUser
from django.contrib.auth.decorators import login_required


@login_required
def like_recipe(request, recipe_id: int):
    recipe = Recipe.objects.get(id=recipe_id)
    like = Like.objects.filter(recipe=recipe, user=request.user).first()

    if not like:
        like = Like.objects.create(recipe=recipe, user=request.user)
        like.save()
        isLiked = True

    else:
        like.delete()
        isLiked = False

    return JsonResponse({'isLiked': isLiked, 'total_likes': recipe.likes.count()})


@login_required
def follow_user(request, user_id: int):
    if request.method == "POST":
        profile_user = get_object_or_404(CustomUser, id=user_id)

        following = False
        if request.user is not profile_user:
            follow = Follow.objects.filter(follower=request.user, followed_user=profile_user).first()

            if not follow:
                Follow.objects.create(follower=request.user, followed_user=profile_user)
                following = True
            else:
                follow.delete()
                following = False

        return JsonResponse({'following': following, 'follower_count': Follow.objects.filter(
            followed_user=profile_user).count(),
                             'following_count': Follow.objects.filter(follower=profile_user).count()})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def review_recipe(request, recipe_id: int):
    if request.method == 'POST':
        body = request.POST.get('review-body')
        rating = request.POST.get('rating');
        recipe = Recipe.objects.get(id=recipe_id)

        Review.objects.create(recipe=recipe, user=request.user, body=body, rating=rating)

        return redirect("recipe:detail", recipe_id=recipe_id)


@login_required
def delete_review(request, review_id: int):
    review = Review.objects.get(id=review_id)
    review.delete()

    return redirect("recipe:detail", recipe_id=review.recipe.id)
