from django.contrib.auth.models import AbstractUser  # actual user data structure
from django.db import models


# modify default user model to interact with database
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)  # media/profile_pictures
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
