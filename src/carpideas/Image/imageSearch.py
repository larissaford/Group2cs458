from .forms import SearchForm
from .models import SearchQuery, ImageURL
from carideas import imageGetter.py
from Image import queue.py
# todo a function that loops over pervious search querys
# todo a function that loops over all images that are associated with the search querry
def class ImageSearch:

	def _init_(self,search, queue):
		self.search = formmat.clean_data.get('search')
		self.queue = ImageQueue()

	def new_user_search_entery(search):
		
		searchquery = form.save(commit = False)
		searchquery.userSearchQuery= form.cleaned_data.get('search')
		searchquery.lastSeached = datetime.now()
		searchquery.User
		
		new_image_url(imageGetter.fetchImage(search),search)
		# there should only be one imgaeURL

		queue.enqueue(ImageURL.objects.get(ImageSearch = search))

		#mass_fill_new(imageGetter.fetchImageMass(search),search)

	def new_image_url(new_image_url, search):
		image = ImageURL
		image.url = new_image
		image.searchQuery = search
		


	def get_one_new_image_url(search, past_image):
		new_url = False
		while new_url == false:
				url = imageGetter(search)
				new_url =compare_image(url, past_image)
		new_image_url(url, search)

		
		
	def mass_fill_new(new_image_url_list, search):
		for each in new_image_url_list:
			new_image_url(new_image_url, search)

	def mass_fill_old(new_image_url_list,search, past_image_list):
		unique_url = list()
		compare_two_list(new_image_url_list,past_image_list)
		for each in unique_url:
			new_image_url(unique_url, search)

	def past_search(self, search):


		past_search =  SearchQuery.objects.filter(searchQuery = search)
		
		if past_search == null:
			# this is a new search
			new_user_search_entery(search)

		else:
			# call past_image retun a list of all past images that have the key value of search
			past_image_list = past_image(search)
			if past_image = null:
				


	# searches past image and sees if the user has any past search that have not been seen
	def past_image(self,search)

		past_image_list =list()
		# create a list of images from past search
		past_image = ImageURL.objects.filter(SearchQuery = search)
		past_image = ImageURL.objects.filter(imageSeeOn = NULL)	
		past_search_list = list(past_image)
		return past_image_list
		
	def compare_image(url,past_image_list):
		url_unique = False
		for each in past_image_list
			if url == past_image_list.url():
				return url_unique
				
		url_unique =True
		return url_unique

	def compare_two_list(list_old,list_new):
		return (list(list(set(list_new)-set(list_old)) + list(set(list_new)-set(list_new))))


