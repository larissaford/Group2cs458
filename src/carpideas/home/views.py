from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello World</h1>")

    #contains a key-value pair
    my_context = {
        "my_text": "this is about me"
    }

    return render(request, "home.html", my_context)