from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teams.models import Team

def hackerboard(request):
    teams = Team.objects.all()
    result = []
    for team in teams:
        t = {}
        t['name'] = team.team_name
        t['solves'], t['score'] = get_team_stats(team)
        result.append(t)
    return render(request, 'home/hackerboard.html', {'teams': result})

def get_team_stats(team):
    users = team.users.all()
    solved_challenges = set()

    for user in users:
        submissions = user.submissions.all()
        for submission in submissions:
            if submission.correct:
                solved_challenges.add(submission.challenge)
    
    num_solved = len(solved_challenges)
    team_score = 0

    for challenge in solved_challenges:
        team_score += challenge.score
    
    return num_solved, team_score