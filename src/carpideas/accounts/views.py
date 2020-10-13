from django.http import HttpResponse # nice for testing
from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

# Create your views here.

# TODO: send confirmation email
# TODO: display success message on login page
# TODO: Possibly encapsulate email process for resending activation email
def register_view(request):
    register_form = RegisterForm()

    if request.method == "POST": # check method
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            register_form.save()

            current_site = get_current_site(request)
            username = register_form.cleaned_data.get('username')
            to_email = register_form.cleaned_data.get('email')
            emailContext = {
                'name': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }

            emailMessage = render_to_string('accounts/email_template.html', emailContext)
            email = EmailMessage(
                'Thank You For Registering!',
                emailMessage,
                settings.EMAIL_HOST_USER,
                [to_email]
                )
            email.fail_silently = False
            email.send()

            # TODO: will have to add code in login page as done at 21:27 in video
            messages.success(request, f"Account was created for {username}. Please check your email for an activation link")

            # create a page informing user to verify email
            #return redirect("login") # redirect to login page

    context = {
        "form": register_form
    }
    return render(request, 'accounts/register.html', context)

# TODO: create "activation link not valid" and redirect to main dashboard page
# Triggered when user registers and clicks on the link sent in email
def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. '
                            'Now you can log into your account')
    else:
        # replace with actual page
        return HttpResponse('Activation link is invalid')
