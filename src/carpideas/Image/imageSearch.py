from .forms import SearchForm
from .models import SearchQuery, ImageURL
# todo a function that loops over pervious search querys
# todo a function that loops over all images that are associated with the search querry
def new_user_search_entery():
	
	searchquery = form.save(commit = False)
	searchquery.userSearchQuery= form.cleaned_data.get('search')
	searchquery.lastSeached = datetime.now()
	searchquery.User

def new_image_url(new_image_url, search):
	image = ImageURL
	image.url = new_image
	image.searchQuery = search


def perviousSearch(self, search):
	#create a list of all past search users
	pastSearch = SearchQuery.objects.all()

	for x in pastSearch:
		# checks if search equals a past search
		if search == pastSearch.userSearchQuery
			
			imagesInPastSearch(search)
		else:
			#creates a new userSearchQuery instance 
			new_user_search_entery()



def imagesInPastSearch(self, search):

	#One check if there are any image url that have not be seen first
	#Two creat a list of urls that have not been seen
	#Three check if there is any images in the past seen images that where liked if so
	#so then add them to the stat
	#if the user has seen the liked image in the past few week then the user should added to the stack 
	#if there is no not seen images then wee need to seen the query to the imagegetter 

	images_in_past_search =  ImageURL.objects.filter(searchQuery = search)
	
	for x in images_in_past_search:
		if images_in_past_search.imageSeenOn ==null:
			q.enqueue(images_in_past_search.url)

	while q.size < 3:
		#call image web scraper 
		#check if the image is is already stored in images_in_past_search
		newImageURLIsU = False
		while(newImageURLIsU ==False )
			newImageURL = imagegetter()
			for x in images_in_past_search:
				if newImageURL == images_in_past_search.url
					break
				else:
					newImageURLIsU= True
					new_image_url(newImageURL)

					break


class checkUserInput:
	perviousSearch(search)
class ImageQueue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
	
	q = ImageQueue