from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterForm

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import CustomUser
# from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login, logout

# For Activation Link
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import login

# For Sending Emails
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# For messaging after registered
from django.contrib import messages


# from django.contrib.messages import constants as messages

# Create your views here.

# TODO: display success message on login page
# TODO: Possibly encapsulate email process for resending activation email
def register_view(request):
    register_form = RegisterForm()
    if request.method == "POST":  # check method
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            register_form.save()

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

            # TODO: will have to add code in login page as done at 21:27 in video
            messages.success(request,
                             f"Account was created for {username}. Please check your email for an activation link")

            # create a page informing user to verify email
            return redirect("login")  # redirect to login page

    context = {
        "form": register_form
    }
    return render(request, 'accounts/register.html', context)


# TODO: create "activation link not valid" and redirect to main dashboard page
# Triggered when user registers and clicks on the link sent in email
def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        # messages.success(request, "Your account is now active!")
        # return redirect('login')
    else:
        # replace with actual page
        messages.error(request, 'Link is no longer valid')
        return redirect('login')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


# Handles logging into service
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.info(request, f"You are now logged in as {username}")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Invalid username or password")
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)
    else:
        return redirect("home")


# TODO: Create and add a template for requesting a password reset
def password_reset_view(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            current_site = get_current_site(request)
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            # associated_users = User.objects.get(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
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
                    print(uid)
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
    password_reset_form = PasswordResetForm()
    context = {
        "form": password_reset_form
    }

    return render(request, 'accounts/password_reset.html', context)
