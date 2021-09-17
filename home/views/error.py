from django.shortcuts import render
from django.views.defaults import page_not_found

def handler400(request, message, *args, **argv):
    return render(request,'home/errors/error.html', status=400)

def handler403(request, message, *args, **argv):
    return render(request,'home/errors/error.html', status=403)

def handler404(request, message, *args, **argv):
    return render(request,'home/errors/error.html', status=404)

def handler500(request, *args, **argv):
    return render(request,'home/errors/error.html', status=500)