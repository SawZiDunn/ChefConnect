from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# change default User Model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("profile_picture", "description")}),
    )


admin.site.register(CustomUser)
