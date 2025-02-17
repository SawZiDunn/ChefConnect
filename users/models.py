from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)  # media/profile_pictures
    description = models.TextField(blank=True, null=True)

    # change raw password entered from admin interface to hashed password
    def save(self, *args, **kwargs):
        if self.pk is None:  # Only hash password when creating a new user
            self.set_password(self.password)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.username
