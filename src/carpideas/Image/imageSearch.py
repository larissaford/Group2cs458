#ImageSearch class - Tracen Vail
#last upddat 11/10/20-00.19.00

from models import SearchQuery, ImageURL
#from carpideas.imageGetter import ImageGetter


from datetime import datetime

class ImageSearch:

	def _init_(self,search):
		self.search = search
		

	# creates a list of past images that have not been seen 

	# past_image - Tracen Vail
	# Created 11/05/2020
	# last update l1/30/2020
	# creates a list of past images that have been not been seen
	def past_image(self,search):
		past_image_list =list()
		# create a list of images from past search
		past_image = ImageURL.objects.filter(SearchQuery = search)
		past_image = ImageURL.objects.filter(imageSeeOn = None)	
		past_image_list = list(past_image)
		return past_image_list	


	# compare_two_list
	# Created 11/05/2020
	# Last Update
	# Paramenter list_old is a list of old urls that are from the database
	# Paramenter list_new is a list of new urls that are from image getter
	# This functions will compare a two list and returns an unigue list of urls that are not in the old list
	def compare_two_list(self, list_old,list_new):
		return (list(list(set(list_new)-set(list_old)) + list(set(list_new)-set(list_old))))


	# compare_image
	# Created 10/20/2020
	# last Update
	# parameter url is the url of the of the new image from image getter 
	# parameter past_image_list is a list of past image searchs objects
	# This functions will compare the new image url to all of the old imageURL url
	def compare_image(self, url,past_image_list):
		url_unique = False
		for each in past_image_list:
			if url == past_image_list.url():
				return url_unique
				
		url_unique =True
		return url_unique

	# new_image_url - Tracen Vail
	# Created 10/20/2020
	# Last Updated 11/20/2020
	# Parameter new_image_url is a url from image getter 
	# Parameter search is the search term that the user has inputed 
	# This fucntion creates a new ImageURL object and saves it to the database
	

	def new_image_url(self,new_image_url, search):
		new_image_url = ImageURL(url = new_image_url,imageSeenOn = None, imageLiked= None, imageDisliked= None,searchQuery=search)
		new_image_url.save()

	# new_user_search_entery
	# Created 10/20/2020
	# Last Updated
	# Parameter search is the search term that the user has inputed
	# this function creates a new SearcQuery opject and saves it to the database
	def new_user_search_entery(self,search):
		searchQuery = SearchQuery(userSearchQuery=search, lastSearched = datetime.now)
		searchQuery.save()
		#imageGetter = ImageGetter(searchQuery.search)
		#self.new_image_url(imageGetter.fetchImage(),search)
		
	#gets a list of image url from the imagegetter and then compares the new image url list that is return from imagegetter to the past image url and then creates a new list 

	# mass_fill
	# Created 11/05/2020
	# Last Updated
	# Parameter past_image_list is list of past image urls 
	# Parameter search is the search term that the user has inputed
	# This function will call the fechALLfunction in image getter that will return a massive list of new url that can be added to the database.
	# The mass_fill will also call the compare_two_list function return a unique list of url that will then be added to the data base

	def mass_fill(self, past_image_list,search):
		unique_url = list()
		imageGetter = ImageGetter(search)
	#	unique_url = self.compare_two_list(imageGetter.fetchaAllImage(),past_image_list) // waiting on imageGetter.fechAll()
		for each in unique_url:
			self.new_image_url(unique_url, search)

	
	# past_search -Tracen Vail
	# Created 10/10/2020
	# Last Update
	# Parameter search is the user input that
	# This function compares the user search to past searches that the user has done
	

	def past_search(self, search):
		print(search)
		past_search = list()
		past_search =  SearchQuery.objects.filter(searchQuery = search)
		

		if past_search == 0:
			# this is a new search
			self.new_user_search_entery(search)

		else:
			# call past_image retun a list of all past images that have the key value of search
			past_image_list = self.past_image(search)
			if past_image_list == 0:
				print("hello")

				
	# searches past image and sees if the user has any past search that have not been seen
	


	


test = ImageSearch()
hello = "hello"
test.past_search(hello)
