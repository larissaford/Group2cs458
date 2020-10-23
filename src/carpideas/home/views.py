from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def home_view(request):
    #return HttpResponse("<h1>Hello World</h1>")

    #user = User.objects.get(id=1)

    #contains a key-value pair
    my_context = {
    #    'username' : user.username
    }
    
    return render(request, "home.html", my_context)