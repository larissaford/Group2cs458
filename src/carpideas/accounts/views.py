from django.http import HttpResponse # nice for testing
from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.

# TODO: send confirmation email
# TODO: display success message on login page
def register_view(request):
    register_form = RegisterForm()

    if request.method == "POST": # check method
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user = register_form.cleaned_data.get('username')
            # TODO: will have to add code in login page as done at 21:27 in video
            messages.success(request, f"Account was create for {user}")
            #return redirect("login") # redirect to login page

    context = {
        "form": register_form
    }
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('register')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 
                    'accounts/login.html',
                    {'form':form})

