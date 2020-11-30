"""carpideas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.tokens import account_activation_token

from django.contrib.auth import views as auth_views
from accounts.views import activate_view, password_reset_view, register_view
from home.views import home_view, pixelate_image
from Image.views import search

urlpatterns = [
    path('admin/', admin.site.urls),

    # Registering Paths
    path('register/', register_view, name="register"),
    path('activate/<uidb64>/<token>', activate_view, name='activate'),
    path('activate_error', activate_view, name='activate_error'),

    # Password Reset Paths
    path('password_reset/', password_reset_view, name="reset_password"),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="reset_password_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",
                                                     token_generator=account_activation_token),
         name='password_reset_confirm'),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name='password_reset_complete'),

    # Logging In/Out Paths
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html",
                                                redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="accounts/login.html"), name="logout"),
    

    path('search/',search,name="search"),

    path('', home_view, name="home"),
    
]
