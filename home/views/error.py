from django.shortcuts import render
from django.views.defaults import page_not_found

def handler500(request, *args, **argv):
    return render(request, template_name='home/error.html', status=500)
def handler404(request, exception):
    return render(request, exception, template_name='home/error.html', status=404)