# ImageGetter Class - Seth Schalinske
# Last Edit: 10/14/2020
#
# regex specific to unsplash.com right now
# unfortunately I can only get 9 images per search right now
# I will have to use selenium instead of requests to get more
# this will require a small rewrite to replace requests with seleneium
# for now though method this should allow us to proceed

import requests
import re
import random

class ImageGetter:
    # initiate the image getter with the search term
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    # method to call to get the image
    def fetchImage(self):
        URL = "https://unsplash.com/s/photos/" + self.searchTerm + "?orientation=landscape" 
        webpage = requests.get(URL)
        imageURLs = re.findall(r'_2VWD4 _2zEKz" (.*?)">', webpage.text) 
        randNum = random.randint(0,8) 
        imageStr = imageURLs[randNum]
        imageURL = imageStr.split('srcSet="')[1].split('?ixlib=')[0]
        return imageURL


# uncomment the code below to test

#ig = ImageGetter("fish")
#url = ig.fetchImage()
#print(url)
#print("done")