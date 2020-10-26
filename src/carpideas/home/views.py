from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from PIL import Image
import urllib.request, base64
import io
import numpy as np
import matplotlib.pyplot as plt


# Create your views here.
def home_view(request):
    #return HttpResponse("<h1>Hello World</h1>")

    #user = User.objects.get(id=1)

    #contains a key-value pair
    my_context = {
    #    'username' : user.username
    }
    
    return render(request, "home.html", my_context)

def pixelate_image(request):
        
    fd = urllib.request.urlopen('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Gibson_ES-175.png/160px-Gibson_ES-175.png')
    image_file = io.BytesIO(fd.read())
    image = Image.open(image_file).convert('LA')
    Xg = np.array(image)
    X = Xg[:,:,0]
    U,s,Vh = np.linalg.svd(X,full_matrices=False)
    S = np.diag(s)
    r = 1
    ldimg = U[:,:r].dot(S[:r,:r]).dot(Vh[:r,:])
    plt.imshow(ldimg)
    plt.savefig('test.png', format='png')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'home.html', {'data':uri})

    my_context={
        'pixelation' : 'cell://test.png'
    }

    return render(request, 'home.html', my_context)