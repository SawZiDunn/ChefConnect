from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

app_name = "recipe"
urlpatterns = [
    path('', index, name="index"),
    path('new/', new, name="new"),
]