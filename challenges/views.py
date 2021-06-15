from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from teams.models import Team
from challenges.models import Challenge, Submission
from django.http import HttpResponse

@login_required(login_url='profile-login')
def challenges(request):
    user = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = user)
    problems = Challenge.objects.all()
    submissions = Submission.objects.filter(user = user)
    return render(request, 'challenges/challenges.html', {'profile':profile, 'challenges':problems, 'submissions':submissions})

@login_required(login_url='profile-login')
def flagsubmit(request):

    if request.method == 'POST':
        challenge_id = request.POST['challenge-id']
        challenge_flag = request.POST['challenge-flag']

        challenge = Challenge.objects.get(id = challenge_id)
        flag = challenge.flag
        points = challenge.score

        if challenge_flag == flag:
            response = '<div id="flag_incorrect"><p>INCORRECT</p></div>'
        else:
            response = '<div id="flag_incorrect"><p>INCORRECT</p></div>'
    else:
        pass
    return HttpResponse('done')