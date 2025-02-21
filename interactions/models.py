from django.db import models
from django.conf import settings
from recipe.models import Recipe


class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.recipe}"


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followings')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.followed_user}"

    # user.followings.all() → Users this user follows
    # user.followers.all() → Users who follow this user


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    body = models.TextField()

    def get_stars(self):
        return range(self.rating)

    def __str__(self):
        return f"{self.user} gave a review on {self.recipe}"
