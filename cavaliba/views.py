# main/views.py

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render



def index(request):
    #return HttpResponse("Hello from Project Index - MAIN index")
    #return render(request, 'myapp1/index.html', {'item': data})
    return render(request, 'main.html')
