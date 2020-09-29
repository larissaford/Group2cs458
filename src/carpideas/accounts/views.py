from django.http import HttpResponse # nice for testing
from django.shortcuts import render

# Create your views here.


def register_view(request):
    print('IN THE CONTROLLER')
    return render(request, 'accounts/register.html', {})

