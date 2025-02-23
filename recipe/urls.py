from django.urls import path

import recipe
from .views import *

app_name = "recipe"

urlpatterns = [
    path('', index, name="index"),  # for home page

    # recipe routes
    path('recipe/new/', add_recipe, name="add_recipe"),
    path('recipe/<int:recipe_id>/', recipe_detail, name="detail"),
    path('recipe/<int:recipe_id>/edit/', edit_recipe, name="edit"),
    path('recipe/<int:recipe_id>/edit/ingredients/', edit_ingredients, name="edit_ingredients"),
    path('recipe/<int:recipe_id>/edit/instructions/', edit_instructions, name="edit_instructions"),
    path('recipe/<int:recipe_id>/delete/', delete, name="delete"),
    path('recipe/<int:recipe_id>/save/', save, name="save"),

    path('recipe/saved/', saved_recipe, name="saved_recipes")
]
