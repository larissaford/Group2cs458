from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Account


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    # username = forms.CharField(max_length=16)
    # password = forms.PasswordInput()
    # email = forms.EmailField()