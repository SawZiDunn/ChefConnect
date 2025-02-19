from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Like, Comment, Follow, Conversation, ConversationMessage
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


@login_required()
def comment_recipe(request, recipe_id: int):
    if request.method == 'POST':
        body = request.POST.get('body')
        recipe = Recipe.objects.get(id=recipe_id)

        Comment.objects.create(recipe=recipe, user=request.user, body=body)

        return redirect("recipe:detail", recipe_id=recipe_id)


@login_required()
def start_conversation(request, user_id: int):
    conversation = Conversation.objects.get(user1=request.usr,
                                            user2=CustomUser.objects.get(id=user_id)) or Conversation.objects.get(
        user1=CustomUser.objects.get(id=user_id), user2=request.user)

    if not conversation:
        Conversation.objects.create(user1=request.user, user2=CustomUser.objects.get(id=user_id))
        return

    messages = conversation.messages.all()

    return
    # conversation = Conversation.objects.filter(
    #     (models.Q(user1=user1) & models.Q(user2=user2)) |
    #     (models.Q(user1=user2) & models.Q(user2=user1))
    # ).first()
