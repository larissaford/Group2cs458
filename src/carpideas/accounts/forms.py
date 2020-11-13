from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User
from accounts.models import CustomUser


# Form to register an account on the site
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

# Form for updating user information in the admin portal
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'last_search'
        ]
