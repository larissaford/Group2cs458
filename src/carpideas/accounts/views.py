from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterForm

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import CustomUser
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login, logout

# For Activation Link
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


# For Sending Emails
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# For messaging after registered
from django.contrib import messages


# Create your views here.

# Handles the Registration Process for New Users
# Sends activation link via email upon successful registration
def register_view(request):
    register_form = RegisterForm()
    if request.method == "POST":  # check method
        register_form = RegisterForm(request.POST)
        # Create a user that is not active
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            register_form.save()

            # Set up context for email message
            current_site = get_current_site(request)
            username = register_form.cleaned_data.get('username')
            to_email = register_form.cleaned_data.get('email')
            email_context = {
                'name': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
            email_message = render_to_string('accounts/emails/email_template.html', email_context)
            email = EmailMessage(
                'Thank You For Registering!',
                email_message,
                settings.EMAIL_HOST_USER,
                [to_email]
            )
            email.fail_silently = False
            email.send()

            messages.success(request,
                             f"Account was created for {username}. "
                             f"Please check your email for an activation link")

            return redirect("login")

    context = {
        "form": register_form
    }
    return render(request, 'accounts/register.html', context)


# Triggered when user registers and clicks on the link sent in email
def activate_view(request, uidb64, token):
    # Try to decode the token and get a user
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    # Decoding Failed or User doesn't exits
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # Update user to active and route to login page
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is now active!")
        return redirect('login')
    else:
        return render(request, 'accounts/activate_fail.html')


# Handles sending password reset/activation emails for users that request it
def password_reset_view(request):
    # Check if user is posting data
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        # Form passes built in checks
        if password_reset_form.is_valid():
            current_site = get_current_site(request)
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))

            # Check if there are users with that email
            if associated_users.exists():
                for user in associated_users:
                    # If user is not active, send activation email
                    if not user.is_active:
                        resend_activation(current_site, user)
                        messages.success(request,
                                         f"Activation link resent for {user.username}. "
                                         f"Please check your email for an activation link")
                        return redirect('login')
                    # Send password reset email
                    else:
                        # Get Data needed for email
                        user_email_address = user.email
                        subject = "Password Reset Requested"
                        email_template_name = "accounts/emails/password_reset_email.html"
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        email_context = {
                            "email": user_email_address,
                            "domain": current_site.domain,
                            "site_name": current_site.name,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            "token": account_activation_token.make_token(user),
                            "protocol": 'http'
                        }
                        email_message = render_to_string(email_template_name, email_context)
                        try:
                            email = EmailMessage(
                                subject,
                                email_message,
                                settings.EMAIL_HOST_USER,
                                [user_email_address]
                            )
                            email.fail_silently = False
                            email.send()
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect("/password_reset/done")

    # First time on page, go to blank Password Reset Page
    password_reset_form = PasswordResetForm()
    context = {
        "form": password_reset_form
    }
    return render(request, 'accounts/password_reset.html', context)


# Sends users an activation email when they are not active during password reset
def resend_activation(current_site, user):
    username = user.username
    to_email = user.email
    email_context = {
        'name': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    }
    email_message = render_to_string('accounts/emails/email_template.html', email_context)
    email = EmailMessage(
        'Thank You For Registering!',
        email_message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    email.fail_silently = False
    email.send()

