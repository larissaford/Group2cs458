from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    # list_display = [field.name for field in CustomUser._meta.get_fields() if field.]
    list_display = [
        'username',
        'password',
        'email',
        'last_search'
    ]

admin.site.register(CustomUser, CustomUserAdmin)