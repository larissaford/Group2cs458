from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
# from django.conf import settings

# Create your models here.
#class Image(models.Model):
 #   imageID = models.CharField(max_length=16, primary_key= True)
  #  url = models.URLField()
   # width = models.IntegerField()
    #height = models.IntegerField()
    #users = models.ManyToManyField(User, related_name='liked_images')
    #users = models.ManyToManyField(User, related_name='skipped_images')
    #def __unicode__(self):
    #    return self.name

# Create your models here.
class SearchQuery(models.Model):
	#what the user is searching
	userSearchQuery = models.CharField(max_length=255,unique =True)
	#when was the last time the user seached this topic
	lastSearched  = models.DateTimeField(auto_now_add=True)
	# this makes this seach unique to the user that is seaching this query
	#userWhoSearched = models.ForeignKey(User, related_name='SearchQuery',on_delete=models.CASCADE)
	
	def create(self, cls, userSearchQuery, lastSearched, userWhoSearched):
		searchQuery = cls(userSearchQuery=userSearchQuery, lastSearched = lastSearched, userWhoSearched= userWhoSearched)
		return searchQuery

class ImageURL(models.Model):
	#url is the url path for the image in its database
	url = models.CharField(max_length=255, unique = True)
	#when was the last time that the user saw this image
	#when ImageSeenOn is Null then that will mean that the user has never seen the image befor
	imageSeenOn= models.DateTimeField(auto_now_add= True)
	#the user will be able to see these again with no time constrain
	imageLiked = models.BooleanField()
	#this will keep track of all the images that the user does not wish to seen again
	imageDisliked = models.BooleanField()
	#this is the foreignkey that links Image url to that of SearchQuery
	searchQuery = models.ForeignKey(SearchQuery, related_name='ImageURL', on_delete=models.CASCADE)

	def create(self, cls, url, imageSeenOn, imageLiked, imageDisliked, searchQuery):
		imageURL = cls(url = url,imageSeenOn = imageSeenOn, imageLiked= imageLiked, imageDisliked= imageDisliked,searchQuery=searchQuery)
		return imageURL