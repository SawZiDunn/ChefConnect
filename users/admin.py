from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # controls how usermodel is displayed in django admin panel

from .forms import CustomUserCreationForm
from .models import CustomUser


# change default User Model Display in admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm  # !need to use CustomerUserCreationForm if we modify UserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("profile_picture", "description")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile", {"fields": ("profile_picture", "description")}),
    )

    def save_model(self, request, obj, form, change):
        # print("save_model() in CustomUserAdmin Class")
        
        if not change:  # New user
            print("New user - pass is hashed")
            raw_password = form.cleaned_data.get('password1')  # Get password from form
            if raw_password:
                obj.set_password(raw_password)
        elif change and "password" in form.changed_data:
            print("Existing user - pass is hashed")
            obj.set_password(obj.password)
        else:
            print("No password change")

        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
