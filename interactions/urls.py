from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('comment/<int:recipe_id>/', views.comment_recipe, name='comment_recipe'),
]
