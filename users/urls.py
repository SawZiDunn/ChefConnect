from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    # authentication
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),

    # for user profile
    path('profile/', profile, name="profile"),
    path('profile/following/', following_users, name="following"),
    path('profile/edit/', edit_profile, name="edit_profile"),
    path('profile/password/', change_password, name="change_password"),

    # for any chef's profile
    path('prifile/chef/<int:chef_id>/', chef_profile, name="chef-profile"),
]
