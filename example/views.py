from django.shortcuts import render
from django.http import HttpResponse, request
def helloworld (request):
    return HttpResponse("Hello World, claudia, ayath, adrian")
# Create your views here.
