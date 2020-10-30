from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from PIL import Image
import urllib.request, base64
import io
import numpy as np
import matplotlib.pyplot as plt
from carpideas.imageGetter import ImageGetter




# Create your views here.
def home_view(request):
    #return HttpResponse("<h1>Hello World</h1>")

    image = ImageGetter("fish").fetchImage()
    pixelatedImage = pixelate_image(image)
    

    #user = User.objects.get(id=1)

    #contains a key-value pair
    my_context = {
    #    'username' : user.username
        'image': image,
        'data': pixelatedImage
    }
    
    return render(request, "home.html", my_context)


def pixelate_image(url):
    
    fd = urllib.request.urlopen(url)
    image_file = io.BytesIO(fd.read())
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
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri