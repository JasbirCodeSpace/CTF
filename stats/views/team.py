from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teams.models import Team

@login_required
def solves_pie_chart(request, teamname):
    team = Team.objects.get(team_name = teamname)
    if not team:
        return JsonResponse(data={'labels': [], 'data': []})

    users = team.users.all()
    labels = ['correct', 'wrong']
    data = []

    correct, wrong = 0, 0
    for user in users:
        correct += user.submissions.filter(correct=True).count()
        wrong += user.submissions.filter(correct=False).count()
    data.append(correct)
    data.append(wrong)

    return JsonResponse(data={'labels': labels, 'data': data})

@login_required
def category_pie_chart(request, teamname):
    team = Team.objects.get(team_name = teamname)
    if not team:
        return JsonResponse(data={'labels': [], 'data': []})
    labels = []
    data = []
    team_submissions = {}
    users = team.users.all()
    team_submissions = set()
    for user in users:
        submissions = user.submissions.filter(correct=True)
        for submission in submissions:
            challenge = submission.challenge
            team_submissions.add(challenge)

    category_count={}
    for challenge in team_submissions:
        category_count[challenge.category.name] = category_count.get(challenge.category.name, 0) + 1

    for name,count in category_count.items():
        labels.append(name)
        data.append(count)

    return JsonResponse(data={'labels': labels, 'data': data})