from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from accounts.forms.profile import SignUpForm

# Sign Up View
def profile_signup(request):
    form = SignUpForm(request.POST)
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
        return render(request, 'accounts/profile-signup.html', {'form': form})
