from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Quote

import random
import cv2
from skimage import io
import os
import requests
import subprocess
from subprocess import call
from PIL import Image
import urllib.request, base64
import numpy as np
import matplotlib.pyplot as plt
from carpideas.imageGetter import ImageGetter





# Create your views here.




def home_view(request):
	#return HttpResponse("<h1>Hello World</h1>")
	randNum = 0 # For testing purposes
	# randNum = random.randint(0,16)
	#user = User.objects.get(id=1)
	posts = Quote.objects.get(quoteID=randNum)
	 
	image_url = ImageGetter("cow").fetchImage()
	print(image_url)
	pixelatedImage = pixelate_image(image_url, "64")

	#user = User.objects.get(id=1)

	#contains a key-value pair
	my_context = {
	#    'username' : user.username
		'image': image_url,
		'data': pixelatedImage,
		'quote': posts.quote
	}
	# Check if user is anonymous user
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "home.html", my_context)


def download_image(image_url):
	
	img_data = requests.get(image_url).content
	with open('image.jpg', 'wb') as handler:
		handler.write(img_data)


def old_pixelate_image(url):
	
	"""
	fd = urllib.request.urlopen(url)
	image_file = io.BytesIO(fd.read())
	image = Image.open(image_file).convert('LA')
	Xg = np.array(image)
	X = Xg[:,:,0]
	U,s,Vh = np.linalg.svd(X,full_matrices=False)
	S = np.diag(s)
	r = 10
	ldimg = U[:,:r].dot(S[:r,:r]).dot(Vh[:r,:])
	fig = plt.figure()
	plt.imshow(ldimg, aspect='equal')
	plt.axis('off')
	plt.savefig('image.png', format='png', bbox_inches=0)
	
	fig = plt.gcf()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	return uri

 """

def pixelate_image(image_url, bitsize):
	 	
	wd = os.getcwd()+"\\home\\"

	image = io.imread(image_url)
	status = cv2.imwrite(wd+"image.png", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	print()
	print("Image written to file-system : ",status)
	
	#pixelation through PyPXL, needs a png file
	#"python pypxl_image.py -s 16 16 image.png pixelated.png"
	bashCommandForPixelation = "python "+wd+"pypxl_image.py -s "+bitsize+" "+bitsize+" "+wd+"image.png "+wd+"pixelated.png" 
	print(bashCommandForPixelation)
	print()
	try:
		process = subprocess.check_call(bashCommandForPixelation.split(),shell=True)
	except subprocess.CalledProcessError:
		print("Update the search term to something that hasn't been used before")
		print()
		return -1

	encoded = base64.b64encode(open(wd+"pixelated.png", "rb").read())
	uri = urllib.parse.quote(encoded)

	return uri
