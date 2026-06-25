from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('<h1>Index page</h1>')

def create(request):
    return HttpResponse({'status': 'ok', 'session': 1})
