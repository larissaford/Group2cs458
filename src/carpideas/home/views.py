from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Quotes
import random

# Create your views here.



def home_view(request):
	#return HttpResponse("<h1>Hello World</h1>")
	randNum = random.randint(0,16) 
	#user = User.objects.get(id=1)
	posts = Quotes.objects.get(quotesID=randNum)
	 
	my_context = {
	#    'username' : user.username
		'quote': posts.quote
	}
	
	return render(request, "home.html", my_context)