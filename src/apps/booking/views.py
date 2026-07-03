import json
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse('<h1>Index page</h1>')

@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
            query = json.loads(request.body)
            return JsonResponse(query)
        except ValueError:
            return JsonResponse({'status': 'error'})
    raise Http404()

def list(request):
    if request.GET:
        return JsonResponse(request.GET)
    raise Http404()