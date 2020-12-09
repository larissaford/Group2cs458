from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
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
import pathlib
import pydantic.json
from pathlib import Path
from django.urls import reverse
from py._path.local import LocalPath


#wanted a stand in for persistant data, but this doesnt work
image = ImageGetter('0').fetchImage()

pydantic.json.ENCODERS_BY_TYPE[pathlib.PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[pathlib.WindowsPath] = str

class Path(pathlib.Path):

    def __new__(cls, *args, **kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        return cls._from_parts(map(str, args))

    def __truediv__(self, other):
        return super().__truediv__(str(other))

class WindowsPath(Path, pathlib.WindowsPath):
    pass
class PosixPath(Path, pathlib.PosixPath):
    pass

# code for testing
def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h1>dataflair</h1>")

# code for testing
def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("dataflair<br> cookie created")
    else:
        response = HttpResponse("Dataflair <br> Your browser does not accept cookies")
    return response

# code for testing
def create_session(request):
	request.session['name'] = 'username'
	request.session['password'] = 'password123'
	print(image)
	request.session['image'] = image
	
	return HttpResponse("<h1>dataflair<br> the session is set</h1>")

# code for testing
def access_session(request):
	response = "<h1>Welcome to Sessions</h1><br>"
	#if request.session.get('image'):
		#response += "image : {0} <br>".format(request.session.get('image'))
	if request.session.get('name'):
		response += "Name : {0} <br>".format(request.session.get('name'))
	if request.session.get('pixelized'):
		response += "Pixelated : {0} <br>".format(request.session.get('pixelized'))
	if request.session.get('password'):
		response += "Password : {0} <br>".format(request.session.get('password'))
	if request.session.get('currentImage'):
		response += "Current Image File : {0} <br>".format(request.session.get('currentImage'))
		#return HttpResponse(response)
	#else:
	#	return redirect('create/')
	return HttpResponse(response)

#code for testing
def delete_session(request):
	try:
		del request.session['name']
		del request.session['password']
		del request.session['image']
		del request.session['pixelized']
		del request.session['currentImage']

	except KeyError:
		pass
	return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")

# assumes that the image exists before downloading
# downloads the currently viewed image stored in the session
def download_view(request):

	path_to_download_folder = str(os.path.join(Path.home(), "Downloads", "image.png"))
	print(path_to_download_folder)
	print()

	if request.session.get('currentImage'):
		image_file = request.session.get('currentImage')
		image_url = getImageURI(image_file)

		randNum = 0 # For testing purposes
		# randNum = random.randint(0,16)
		#user = User.objects.get(id=1)

		posts = Quote.objects.get(quoteID=randNum)

		download_request = True

		my_context = {
		#    'username' : user.username
			'image': image_url,
			'quote': posts.quote,
			'isDownload': download_request
		}
		
		print('Beginning file download with urllib2...')
		path_to_download_folder = str(os.path.join(Path.home(), "Downloads", "image.png"))

		#print(path_to_download_folder)
		image = io.imread(image_file)
		#image = image_url
		status = cv2.imwrite(path_to_download_folder, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
		print("Image written to file-system at ",path_to_download_folder,": ", status)	

	else:
		print ("Image does not exist")
	
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return HttpResponseRedirect(reverse('home'))

def pixelate_view(request):
	bitsize = "64"
	if request.session.get('pixelized'):
		pixelatedImage = request.session.get('pixelized')
		print('session worked ')
		print()
	else:
		#To-do: make this not hard coded
		if request.session.get('image'):
			image_url = request.session.get('image')
			request.session['pixelized'] = pixelate_image(image_url, bitsize)
			pixelatedImage = request.session.get('pixelized')

			print('session created')
			print()
		else:
			pixelatedImage = getImageURI(getFile(os.getcwd()+"\\home\\","pixelated.png"))

	#used for downloading the currently viewed image
	request.session['currentImage'] = getFile(os.getcwd()+"\\home\\", "pixelated.png")
	
	#pixelatedImage = pixelate_image(image._image, bitsize)
	#pixelatedImage = getPixelatedImage()
	#pixelatedImage = old_pixelate_image(image._image)

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

	image_url = getImage(request, image)
	request.session['currentImage'] = getFile( os.getcwd()+"\\home\\" , "image.png")
	print()
	print (request.session.get('currentImage'))
	print()

		
		#LARISSA TO-DO: make it so that pixelation runs in the background and home view runs without waiting,
		# but clicking on the pixelate button still waits in case pixelation wasn't done yet. 
		
	#return HttpResponse("<h1>Hello World</h1>")
	randNum = 0 # For testing purposes
	# randNum = random.randint(0,16)
	#user = User.objects.get(id=1)

	download_request = False

	posts = Quote.objects.get(quoteID=randNum)

	

	#get this from the user
	bitsize = "64"
	 
	#image_url = "https://images.unsplash.com/photo-1604864708171-b6a408b4cba2?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80"
	#print(image_url)
	#pixelatedImage = pixelate_image(image_url, bitsize)

	
		
	#print(image_url)
	
	#user = User.objects.get(id=1)

	#contains a key-value pair
	my_context = {
	#    'username' : user.username
		'image': image_url,
		'quote': posts.quote,
		'isDownload': download_request
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

	wd = os.getcwd()+"\\home\\" #uses the current working directory so that it works with others computers

	#if os.path.exists(wd+"pixelated.png"):
	#	os.remove(wd+"pixelated.png")

	#sanitize bitsize for extra security against shell injection
	bitsize = shlex.quote(bitsize)
	#print(image_url)
	#add a check to see if the image has already been written
	
	#writeImageToFile(image_url, wd)

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

	return getImageURI(getFile(os.getcwd()+"\\home\\","pixelated.png"))

def writeImageToFile(image_url, wd):
	image = io.imread(image_url) #from the scikit-image package (the import statement skimage), makes the url into an image png file
	status = cv2.imwrite(wd+"image.png", cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) #writes the image png file into the file system as image.png

	#testing that the image was written to the file system under the home folder
	print()
	print("Image written to file-system at ",wd,": ", status)

# either gets the image or creates the image
def getImage(request, image_url):
	if request.session.get('image'):
		image = request.session.get('image')
		print('session worked ')
		#print(image)
		print()
	else:
		print('setting new image')
		wd = os.getcwd()+"\\home\\"
		writeImageToFile(image_url, wd)
		request.session['image'] = getImageURI(getFile(wd, "image.png"))
		image = request.session.get('image')

	return image

def getImageURI(filename):
	#filename = os.getcwd()+"\\home\\" + imageName #uses the current working directory so that it works with others computers

	ext = filename.split('.')[-1]
    
	prefix = f'data:image/{ext};base64,'
	with open(filename, 'rb') as f:
		img = f.read()
    
	return prefix + base64.b64encode(img).decode('utf-8')

def search(request):
	print("Hello world ")

def getFile(filePath, filename):
	pathlib.Path(filePath, filename)