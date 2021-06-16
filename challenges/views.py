from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from teams.models import Team
from challenges.models import Challenge, Submission
from django.http import HttpResponse, JsonResponse

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
            prev_submission = Submission.objects.get(challenge = challenge, user = request.user)
            if prev_submission and prev_submission.correct:
                response = 'Already Submitted'
            else:
                flag_submission = Submission(challenge = challenge, user = request.user, correct = True)
                flag_submission.save()

                initial_score = Profile.objects.get(user = request.user).score
                new_score = initial_score + points
                Profile.objects.filter(user = request.user).update(score = new_score)
                response = 'Correct'
        else:
            response = 'Incorrect'
    else:
        response = 'Invalid Request'
    return JsonResponse({'msg': response})