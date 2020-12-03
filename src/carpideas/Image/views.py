from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import SearchQuery
from .models import Image
from django.views.generic import ListView
#form .forms import SearchForm // will add this later
from imageSearch import imageSearch

import request
# Create your views here.

class HomePageView(ListView):
	model = Image
	template_name = 'home.html'


#def user_input(request, pk):
#def search(request):
