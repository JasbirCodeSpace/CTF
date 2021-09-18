from django.shortcuts import render
from .hackerboard import hackerboard
from .error import handler404, handler500

def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def instructions(request):
    return render(request, 'home/instructions.html')
