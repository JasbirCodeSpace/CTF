from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from accounts.forms.profile import RegisterForm, LoginForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User

def profile_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data.get('name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('accounts/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'shikhawat.jasbir@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')

            user = authenticate(username= username, password= password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/profile-register.html', {'form': form})

def profile_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def profile_login(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/profile-login.html', {'form':form})
    
@login_required
def profile_view(request):
    id = request.GET.get('id', None)
    if id is None:
        id = request.user.id
    user = User.objects.get(id=id)
    team = user.profile.team.team_name
    if not team:
        team = "None"
    score = user.profile.score
    solves = user.profile.submissions.filter(correct=True)

    return render(request, 'accounts/profile.html', {'team':team, 'score': score, 'solves': solves})
