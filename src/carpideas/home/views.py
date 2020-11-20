from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from accounts.models import CustomUser
from .models import Quote
from carpideas.imageGetter import ImageGetter

from requests.auth import HTTPBasicAuth

import shutil
from PIL import Image
import random
import cv2
from io import BytesIO
from skimage import io
import os
import requests
import subprocess
import shlex
import base64, urllib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class ImageClass:
	def __init__(self, image='0'):
	   self._image = ImageGetter(image).fetchImage()

	@property 
	def GetImage(self):
		return self.__image

	@GetImage.setter
	def GetImage(self, name):
		self.__image = ImageGetter(name).fetchImage()


image = ImageClass()

def download_view(request):

	global image

	image_url = image._image

	img_data = requests.get(image_url, auth=HTTPBasicAuth('user', 'pass')).content

	randNum = 0 # For testing purposes
	# randNum = random.randint(0,16)
	#user = User.objects.get(id=1)

	posts = Quote.objects.get(quoteID=randNum)

	my_context = {
	#    'username' : user.username
		'image': image_url,
		'quote': posts.quote
	}
	
	print('Beginning file download with urllib2...')
	path_to_download_folder = str(os.path.join(Path.home(), "Downloads", "image.png"))

	image = io.imread(image_url)
	status = cv2.imwrite(path_to_download_folder, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	print("Image written to file-system at ",path_to_download_folder,": ", status)		
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "home.html", my_context)


def pixelate_view(request):
	bitsize = "64"
	#pixelatedImage = pixelate_image(image._image, bitsize)
	#pixelatedImage = getPixelatedImage()
	pixelatedImage = old_pixelate_image(image._image)

	my_context = {
	#    'username' : user.username
		'pixelated': pixelatedImage
	}
	# Check if user is anonymous user
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "pixelated.html", my_context)

def home_view(request):

	global image
	#return HttpResponse("<h1>Hello World</h1>")
	randNum = 0 # For testing purposes
	# randNum = random.randint(0,16)
	#user = User.objects.get(id=1)

	posts = Quote.objects.get(quoteID=randNum)

	#LARISSA TO-DO: make it so that pixelation runs in the background and home view runs without waiting,
	# but clicking on the pixelate button still waits in case pixelation wasn't done yet. 

	#get this from the user
	bitsize = "64"
	 
	image_url = image._image #to-do: call setter
	#print(image_url)
	
	#user = User.objects.get(id=1)

	#contains a key-value pair
	my_context = {
	#    'username' : user.username
		'image': image_url,
		'quote': posts.quote
	}
	# Check if user is anonymous user
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "home.html", my_context)
		

def old_pixelate_image(url):
	
	fd = urllib.request.urlopen(url)
	image_file = BytesIO(fd.read())
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
	buf = BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	prefix = f'data:image/;base64,'
	return prefix + base64.b64encode(buf.read()).decode('utf-8')

# this function returns a URI that is used for displaying the pixelated image
# this function takes a url for the image that wants to be pixelated
# this function takes a bitsize for the number of bits it should be pixelated to
def pixelate_image(image_url, bitsize):

	

	#sanitize bitsize for extra security against shell injection
	bitsize = shlex.quote(bitsize)
	wd = os.getcwd()+"\\home\\" #uses the current working directory so that it works with others computers

	if os.path.exists(wd+"pixelated.png"):
		os.remove(wd+"pixelated.png")

	image = io.imread(image_url) #from the scikit-image package (the import statement skimage), makes the url into an image png file
	status = cv2.imwrite(wd+"image.png", cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) #writes the image png file into the file system as image.png

	#testing that the image was written to the file system under the home folder
	print()
	print("Image written to file-system at ",wd,": ", status)
	
	#pixelation through PyPXL, needs a png file
	#uses bitsize to determine the bitsize of the image
	#subprocess uses multithreading
	bashCommandForPixelation = "python "+wd+"pypxl_image.py -s "+bitsize+" "+bitsize+" "+wd+"image.png "+wd+"pixelated.png" 
	print(bashCommandForPixelation)
	print()
	#test whether the subprocess works or returns an error
	try:
		process = subprocess.check_call(bashCommandForPixelation.split(),shell=True)
	except subprocess.CalledProcessError:
		print("Try refreshing the page or update the search term to something that hasn't been used before")
		print()
		return -1

	return getPixelatedImage()

def getPixelatedImage():
	filename = os.getcwd()+"\\home\\" + "pixelated.png" #uses the current working directory so that it works with others computers

	ext = filename.split('.')[-1]
    
	prefix = f'data:image/{ext};base64,'
	with open(filename, 'rb') as f:
		img = f.read()
    
	return prefix + base64.b64encode(img).decode('utf-8')