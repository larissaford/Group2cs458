from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.

# Custom admin model (because we are not using Django's default user)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'password',
        'email',
        'last_search'
    ]

# Register CustomUser and CustomAdmin for use in Admin page
admin.site.register(CustomUser, CustomUserAdmin)