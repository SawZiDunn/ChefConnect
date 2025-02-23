from django.urls import path

import recipe
from .views import *

app_name = "recipe"

urlpatterns = [
    path('', index, name="index"),
    path('recipe/new/', add_recipe, name="add_recipe"),
    path('recipe/<int:recipe_id>/', recipe_detail, name="detail"),
    path('recipe/edit-recipe/<int:recipe_id>/', edit_recipe, name="edit"),
    path('recipe/edit-ingredients/<int:recipe_id>/', edit_ingredients, name="edit_ingredients"),
    path('recipe/edit-instructions/<int:recipe_id>/', edit_recipe, name="edit_instructions"),
    path('recipe/delete/<int:recipe_id>/', delete, name="delete"),
    path('recipe/save/<int:recipe_id>/', save, name="save"),
    path('recipe/saved/', saved_recipe, name="saved_recipe")
]
