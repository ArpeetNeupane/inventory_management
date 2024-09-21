from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponse("Hello")