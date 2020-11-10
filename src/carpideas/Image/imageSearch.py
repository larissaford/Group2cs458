
from models import SearchQuery, ImageURL
from carpideas.imageGetter import ImageGetter
from Image.queue import ImageQueue

from datetime import datetime

class ImageSearch:

	def _init_(self,search, queue):
		self.search = search
		self.queue = ImageQueue()

	# creates a list of past images that have not been seen 
	def past_image(self,search):
		past_image_list =list()
		# create a list of images from past search
		past_image = ImageURL.objects.filter(SearchQuery = search)
		past_image = ImageURL.objects.filter(imageSeeOn = None)	
		past_image_list = list(past_image)
		return past_image_list	


	# compares two list and returns a new list of urls
	def compare_two_list(self, list_old,list_new):
		return (list(list(set(list_new)-set(list_old)) + list(set(list_new)-set(list_old))))


	# i dont think i need this methond any more
	def compare_image(self, url,past_image_list):
		url_unique = False
		for each in past_image_list:
			if url == past_image_list.url():
				return url_unique
				
		url_unique =True
		return url_unique
	# creates and saves a new Image URL to the data base
	def new_image_url(self,new_image_url, search):
		new_image_url = new_image_url(url = new_image_url,imageSeenOn = None, imageLiked= None, imageDisliked= None,searchQuery=search)
		new_image_url.save()

	# creates a new object of SearchQuery and saves it to the datebase
	def new_user_search_entery(self,search):
		searchQuery = SearchQuery(userSearchQuery=search, lastSearched = datetime.now)
		searchQuery.save()
		imageGetter = ImageGetter(searchQuery.search)
		self.new_image_url(imageGetter.fetchImage(),search)
		
	#gets a list of image url from the imagegetter and then compares the new image url list that is return from imagegetter to the past image url and then creates a new list 

	def mass_fill(self, past_image_list,search):
		unique_url = list()
		imageGetter = ImageGetter(search)
	#	unique_url = self.compare_two_list(imageGetter.fetchaAllImage(),past_image_list) // waiting on imageGetter.fechAll()
		for each in unique_url:
			self.new_image_url(unique_url, search)

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
