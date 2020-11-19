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


def user_input(request, pk):
	
	# 
	# First check if the request is a POST or a GET
	if request.method =='POST'

		# passes the "search query to the serve
		#form = SearchForm(request.POST)

		# Asking Django to verify the data
		# Asking Django to verify the form
		#if form.is_valid():
		
			ig = ImageSearch()

			ig.past_search= form.clean_data.get('')
		
		# not valiad input
		else:
			form = SearchForm()
		#return the user back to an empty search bar
		return render(request,"search.html",{'form':form})
	# The below code block will create a new instance of the user's search 
	# This is done after "search" is compared to previous "searches"

	
