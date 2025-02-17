from django.urls import path, include

import recipe
from .views import *

app_name = "recipe"

urlpatterns = [
    path('', index, name="index"),
    path('recipe/new/', add_recipe, name="add_recipe"),
    path('recipe/<int:recipe_id>', recipe_detail, name="detail"),
    path('recipe/edit/<int:recipe_id>', edit, name="edit"),
    path('recipe/delete/<int:recipe_id>', delete, name="delete"),
]
