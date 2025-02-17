from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('profile', profile, name="profile"),
    path('chef-profile/<int:chef_id>', chef_profile, name="chef-profile"),
    path('edit-profile', edit_profile, name="edit_profile"),
]
