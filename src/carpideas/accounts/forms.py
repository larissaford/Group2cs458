from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User
from accounts.models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'last_search'
        ]
