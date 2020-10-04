from django.http import HttpResponse # nice for testing
from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm

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

