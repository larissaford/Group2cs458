# ImageGetter Class - Seth Schalinske
# Last Edit: 11/11/2020
#
# regex used is specific to unsplash.com
# 
# be sure to install selenium with "pip install selenium"

import requests
import re
import random
import time
from selenium import webdriver

class ImageGetter:

    # Initiate the image getter with the search term and search URL (created using the searchTerm)
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm
        self.URL = "https://unsplash.com/s/photos/" + searchTerm + "?orientation=landscape" 

    # Method to return a single image url by getting the first several image URLs and selecting one at random
    def fetchImage(self):

        webpage = requests.get(self.URL)                                                                
        imageURLs = re.findall(r'_2UpQX" (.*?)">', webpage.text)                                        # find URLs in HTML
        randNum = random.randint(0,len(imageURLs))                                                      
        
        if imageURLs:                                                                                   # make sure an image to display to the user was found
            imageStr = imageURLs[randNum]
            imageURL = imageStr.split('srcSet="')[1].split('?ixid=')[0]                                # clean up URL string
            return imageURL
        else:
            return 'https://source.unsplash.com/random/1920x1080'                                       # get a random image if no URL is found above


    # Method to return a list of images to populate the database using selenium to load more of the infinite scroll page
    def fetchAllImages(self):
        
        # TODO: Check user system to automatically select a chromedriver to run

        # For now the user must change the path manually to their version of chromedriver.
        # You can download chromedriver at: https://chromedriver.chromium.org/downloads  
        # Be sure you select the correct driver for your version of chrome
        
        # For example I have placed my version of chromedriver at: /Users/sethschalinske/Desktop/chromedriver
        # To easily select the path to chromedriver on Windows, Shift Right Click on the executable and select Copy as Path
        driver = webdriver.Chrome(executable_path="/Users/sethschalinske/Desktop/chromedriver")
        driver.get(self.URL)                                                                            
        time.sleep(2)                                                                                   # wait X seconds for page load before running javascript
        
        screen_height = driver.execute_script("return window.screen.height;")                           
        scroll_pause_time = .5                                                                          # time to wait before scrolling again
        scrolls = 2                                                                                     # number of scrolls to execute
        screenMultiplier = 1                                                                            # multiplier to determine where to scroll to next

        for i in range(0, scrolls):
            driver.execute_script("window.scrollTo(0, {screen_height}*{screenMultiplier});".format(screen_height=screen_height, screenMultiplier=screenMultiplier)) # execute scroll
            time.sleep(scroll_pause_time)
            screenMultiplier = screenMultiplier + 1                                                     
        
        time.sleep(2)                                                                                   # wait X seconds for page to finish loading before 
        webpage = driver.page_source                                                                    # getting the webpage 
        imageURLs = re.findall(r'_2zEKz" (.*?)">', webpage)                                             # find URLs in HTML
        
        returnURLs = []

        for url in imageURLs:
            
            imageURL = re.search("(?P<url>https?://[^\s]+)", url).group("url")                          # clean up URL string
            returnURLs.append(imageURL)                                                                 # and add it to the return list

        return returnURLs


# FUNCTIONALITY TESTS: 


# uncomment the code below to test fetchImage (Ctrl + /)
ig = ImageGetter("fish")
url = ig.fetchImage()
print(url)
print("done")

# uncomment the code below to test fetchAllImages  (Ctrl + /)
# ig = ImageGetter("fish")
# urls = ig.fetchAllImages()
# for u in urls:
#     print(u)
# print("\nNumber of images found: " + str(urls.__len__()))
# print("done")