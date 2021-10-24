from django.shortcuts import render
from django.views.defaults import page_not_found

def handler400(request, exception):
    return render(request,'home/errors/error.html', {'exception': '400 Bad Request'}, status=400)

def handler403(request, exception):
    return render(request,'home/errors/error.html', {'exception': exception}, status=403)

def handler404(request, exception):
    return render(request,'home/errors/error.html', {'exception': '404 Page Not Found'}, status=404)

def handler500(request,  *args, **argv):
    return render(request,'home/errors/error.html', {'exception': '500 Internal Server Error'}, status=500)
