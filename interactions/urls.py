from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('review/<int:recipe_id>/', views.review_recipe, name='review_recipe'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
