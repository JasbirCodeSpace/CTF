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
def completed(request):
    return render(request, 'challenges/completed.html')
    
@login_required(login_url='profile-login')
def challenges(request):

    user = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = user)
    submissions =  Submission.objects.filter(user = profile, correct = True)
    solves = set()
    for submission in submissions:
        solves.add(submission.challenge)
    challenges = {}
    categories = ['BLOCKCHAIN', 'WEB', 'FORENSIC', 'CRYPTO', 'REV', 'MISC']
    for category in categories:
        challenges[category] = Challenge.objects.filter(category__name=category).order_by('score')

    return render(request, 'challenges/challenges.html', {'profile':profile, 'categories': challenges, 'submissions': solves})

@login_required(login_url='profile-login')
def flagsubmit(request):

    if request.method == 'POST':
        challenge_id = request.POST['challenge-id']
        challenge_flag = request.POST['challenge-flag']

        challenge = Challenge.objects.get(id = challenge_id)
        user_profile = Profile.objects.get(user = request.user)
        team = user_profile.team

        flag = challenge.flag
        points = challenge.score
        prev_submission = Submission.objects.filter(challenge = challenge, user = user_profile, correct = True)
        _, _, team_challenges, _ = team_details(team) if team else None, None, None, None

        if prev_submission.first():
            response = 'Already submitted'

        elif team_challenges and challenge in team_challenges:
                response = 'Already submitted by team'

        elif challenge_flag == flag:
            flag_submission = Submission(challenge = challenge, user = user_profile, correct = True)
            flag_submission.save()

            initial_score = Profile.objects.get(user = request.user).score
            new_score = initial_score + points
            Profile.objects.filter(user = request.user).update(score = new_score)
            response = 'Correct'
        else:
            flag_submission = Submission(challenge = challenge, user = user_profile, correct = False)
            flag_submission.save()
            response = 'Incorrect'
    else:
        response = 'Invalid Request'
    return JsonResponse({'msg': response})

def get_challenge_submissions():
    challenges = Challenge.objects.all()
    result = {}
    for challenge in challenges:
        result[challenge] = challenge.solves.all()
        print(challenge.solves.all())
        print(challenge.solves.filter(correct=True))
    return result

def team_details(team):
    users = team.users.all()
    team_submissions = {}

    for user in users:
        submissions = user.submissions.filter(correct=True)
        for submission in submissions:
            challenge = submission.challenge
            if challenge not in team_submissions:
                team_submissions[challenge] = submission
            elif challenge in team_submissions and submission.timestamp<team_submissions[challenge].timestamp:
                team_submissions[challenge] = submission
    
    num_solved = len(team_submissions)
    team_score = 0

    submissions = []
    challenges = []
    for challenge, submission in team_submissions.items():
        team_score += challenge.score
        submissions.append(submission)
        challenges.append(challenge)
    
    return users,submissions, challenges, team_score