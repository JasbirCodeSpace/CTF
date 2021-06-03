from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from teams.models import Team
from challenges.models import Challenge, Submission

@login_required(login_url='profile-login')
def challenges(request):
    user = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = user)
    problems = Challenge.objects.all()
    submissions = Submission.objects.filter(user = user)
    return render(request, 'challenges/challenges.html', {'profile':profile, 'challenges':problems, 'submissions':submissions})
