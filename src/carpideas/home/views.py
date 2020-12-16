from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from accounts.models import CustomUser
from .models import Quote
from carpideas.imageGetter import ImageGetter
from django.views.static import serve
from wsgiref.util import FileWrapper
from Image.models import SearchQuery, ImageURL
from requests.auth import HTTPBasicAuth
from Image.forms import searchForm

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
#import pydantic.json
from pathlib import Path
from django.urls import reverse
#from py._path.local import LocalPath
from ftplib import FTP
import mimetypes






#used for making this code work for different operating systems.
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

# code for testing whether browser accepts sessions
def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h1>dataflair</h1>")

# code for testing whether browser accepts sessions
def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("dataflair<br> cookie created")
    else:
        response = HttpResponse("Dataflair <br> Your browser does not accept cookies")
    return response

# code for testing session data
def create_session(request):
	#to-do: add more relevant things to the session, like "image" or "pixelized"
	request.session['name'] = 'username'
	request.session['password'] = 'password123'
	return HttpResponse("<h1>dataflair<br> the session is set</h1>")

# code for testing session data
def access_session(request):
	response = "<h1>Welcome to Sessions</h1><br>"
	if request.session.get('name'):
		response += "Name : {0} <br>".format(request.session.get('name'))
	if request.session.get('image'):
		response += "Image : {0} <br>".format(request.session.get('image'))
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

#code for testing session data, logging out also does this but better. 
# to-do: this is a little bit buggy for some reason
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

# assumes that the current image has been set before downloading
# downloads the currently viewed image stored in the session
def download_view(request):

	path_to_download_folder = os.path.join(Path.home(), "Downloads", "image.png")
	
	if request.session.get('currentImage'):
		print("Current image has been set. Starting download to: ", path_to_download_folder)
		print()
		image_file = request.session.get('currentImage')
		
		#for displaying the current image
		image_url = getImageURI(image_file)

		#not used: for displaying a quote from the database
		randNum = 0 # For testing purposes
		posts = Quote.objects.get(quoteID=randNum)

		my_context = {
			'image': image_url,
			'quote': posts.quote,
			'isDownload': True
		}

	else:
		print ("Current image has not been set. Try reloading the home page")
	
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		wrapper = FileWrapper(open(image_file,"rb"))
		response = HttpResponse(wrapper, content_type='image/jpeg')
		response['Content-Disposition']='attachment; filename=image.png'
		return response
		

#called by pixelation button for pixelizing the current image
def pixelate_view(request):
	#To-Do: bitsize should be received from the user
	bitsize = "64"

	randNum = 0 # For testing purposes
	posts = Quote.objects.get(quoteID=randNum)

	if request.session.get('pixelized'):
		pixelatedImage = request.session.get('pixelized')
		print('pixelized image was stored in session')
		print()
		pixelatedImageFile = str(pathlib.Path(os.getcwd(),"home","pixelated.png"))
		request.session['currentImage'] = pixelatedImageFile
	else:
		if request.session.get('image'):
			print("image found in session for pixelation. pixelation starting now")
			image_url = request.session.get('image')
			
			pixelatedImage = pixelate_image(image_url, bitsize)
			pixelatedImageFile = str(pathlib.Path(os.getcwd(),"home","pixelated.png"))
			#comment this out for testing and uncomment below if pixelation has already completed
			request.session['pixelized'] = pixelatedImage
			request.session['currentImage'] = pixelatedImageFile
			#uncomment this for testing
			#request.session['pixelized'] = getImageURI(pathlib.Path(os.getcwd(),"home","pixelated.png"))	
		else:
			try: #relies on an image already having been pixelized, may return an error
				pixelatedImageFile = str(pathlib.Path(os.getcwd(),"home","pixelated.png"))
				pixelatedImage = getImageURI(pixelatedImageFile)
				#used for downloading the currently viewed image
				request.session['currentImage'] = pixelatedImageFile
			except:
				print("image needs to be set first. load home page and try again.")

	# for testing pixelation functions:
	#pixelatedImage = pixelate_image(image._image, bitsize)
	#pixelatedImage = getPixelatedImage()
	#pixelatedImage = old_pixelate_image(image._image)

	my_context = {
		'image': pixelatedImage,
		'quote': posts.quote,
		'isPixelate': True
	}
	# Check if user is anonymous user
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "home.html", my_context)

def unpixelate_view(request):
	return redirect(home_view)

def home_view(request):

	image_url = getImage(request)

	#set current image for downloading the current image
	request.session['currentImage'] = str(pathlib.Path(os.getcwd(),"home", "image.png"))
		
	randNum = 0 # For testing purposes
	posts = Quote.objects.get(quoteID=randNum)

	#TO-DO: get this from the user
	bitsize = "64"
	
	#contains key-value pairs for inputting variables into HTML
	my_context = {
		'image': image_url,
		'quote': posts.quote,
		'isPixelate': False
	}
	# Check if user is anonymous user
	if not request.user.is_authenticated:
		return redirect("login")
	else:
		return render(request, "home.html", my_context)
		
#uses linear algebra for pixelation, currently not being used anywhere
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
# this function assumes that an image has already been loaded to the file system in the current working directory's home folder
def pixelate_image(image_url, bitsize):

	#arguments for pixelation through PyPXL, which takes an image file and puts the result in a pixelized image file
	# for bitsize, sanitize bitsize for extra security against shell injection because shell=True with the subprocess call
	bitsize = shlex.quote(bitsize) 											#bitsize for the size of the pixelation (i.e. 16x16 or making a 16 bit image)	
	path_Pypxl = str(pathlib.Path(os.getcwd(), "home", "pypxl_image.py")) 	#the python program for pixelizing the image
	path_image = str(pathlib.Path(os.getcwd(), "home", "image.png")) 		#the image being pixelized
	path_pixel = str(pathlib.Path(os.getcwd(), "home", "pixelated.png"))	#where the pixelized result is put

	#subprocess uses multithreading
	bashCommandForPixelation = "python "+path_Pypxl+" -s "+bitsize+" "+bitsize+" "+path_image+" "+path_pixel 
	print(bashCommandForPixelation)
	print()
	try: #test whether the subprocess works or returns an error
		process = subprocess.check_call(bashCommandForPixelation.split(),shell=True)
	except subprocess.CalledProcessError:
		print("Pixelation failed")
		print()
		return -1
	#pixelation succeeded, return the URI for displaying in HTML
	return getImageURI(pathlib.Path(os.getcwd(),"home","pixelated.png"))

# either gets the image or creates the image
def getImage(request):
	if request.session.get('image'):
		print("image found in session")
		image = request.session.get('image')
	else:
		print('setting new image')
		#get image
		image = ImageGetter('0').fetchImage()
	
		print('writing image to files')
		#write image to file
		image = io.imread(image) #from the scikit-image package (the import statement skimage), makes the url into an image png file
		status = cv2.imwrite(str(pathlib.Path(os.getcwd(),"home","image.png")), cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) #writes the image png file into the file system as image.png
		print("Image written to file-system: ", status)

		#set image in session
		image = getImageURI(pathlib.Path(os.getcwd(),"home", "image.png"))
		request.session['image'] = image

		#LARISSA TO-DO: using multithreading, make it so that pixelation runs in the background and home view runs without waiting,
		# but clicking on the pixelate button still waits in case pixelation wasn't done yet. 
		

	return image

#used for displaying images in HTML
def getImageURI(filename):
	prefix = "data:image/;base64,"
	with open(filename, 'rb') as f:
		img = f.read()
	
	return prefix + base64.b64encode(img).decode('utf-8')

def search(request):

	search_form = searchForm()
	if request.method =="POST":
		print("check1")
		search_form = searchForm(request.POST)


		if search_form.is_valid():
			print("Hello world ")
			print("found")
			query = search_form.cleaned_data.get('search')
			print(query)

			print('setting new image')
		#get image

			qrw =""

			qrw.join(query)

			image = ImageGetter(qrw).fetchImage()
	
			print('writing image to files')
		#write image to file
			image = io.imread(image) #from the scikit-image package (the import statement skimage), makes the url into an image png file
			status = cv2.imwrite(str(pathlib.Path(os.getcwd(),"home","image.png")), cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) #writes the image png file into the file system as image.png
			print("Image written to file-system: ", status)

		#set image in session
			image = getImageURI(pathlib.Path(os.getcwd(),"home", "image.png"))
			request.session['image'] = image

			#set current image for downloading the current image
			request.session['currentImage'] = str(pathlib.Path(os.getcwd(),"home", "image.png"))
				
			randNum = 0 # For testing purposes
			posts = Quote.objects.get(quoteID=randNum)

			#TO-DO: get this from the user
			bitsize = "64"
			
			#contains key-value pairs for inputting variables into HTML
			my_context = {
				'image': image,
				'quote': posts.quote,
				'isPixelate': False
			}
			# Check if user is anonymous user
			if not request.user.is_authenticated:
				return redirect("login")
			else:
				return render(request, "home.html", my_context)
		
			