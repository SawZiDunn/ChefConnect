from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [

    path("recipe/<int:recipe_id>/like/", views.like_recipe, name="like_recipe"),
    path("user/<int:user_id>/follow/", views.follow_user, name="follow_user"),

    path("recipe/<int:recipe_id>/review/", views.review_recipe, name="review_recipe"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
]
