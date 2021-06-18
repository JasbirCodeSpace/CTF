from django.shortcuts import render
from .hackerboard import hackerboard

def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')