from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
