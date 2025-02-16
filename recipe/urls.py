from django.urls import path, include

import recipe
from .views import *

app_name = "recipe"
urlpatterns = [
    path('', index, name="index"),
    path('new/', add_recipe, name="add_recipe"),
    path('recipe/<int:recipe_id>', recipe_detail, name="detail"),
]