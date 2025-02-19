from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms


# change default user creation form from django admin interface, no styling
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_picture", "description")


# change default user change form from django admin interface, no styling
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_picture", "description")


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. "
                    "Note that both fields may be case-sensitive.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser

        fields = ("username", "email", "password1", "password2", "profile_picture", "description")

    # Add your custom field widgets here
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Tell us about yourself',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
