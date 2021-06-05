from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from accounts.forms.profile import RegisterForm, LoginForm

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
    