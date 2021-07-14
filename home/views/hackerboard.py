from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teams.models import Team
from django.db.models import Count, Max

def hackerboard(request):
    set_team_scores()
    teams = Team.objects.raw("SELECT id FROM teams_team GROUP BY college_name ORDER BY score DESC LIMIT 1")
    result = []
    for team in teams:
        t = {}
        t['college'] = team.college_name
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

def set_team_scores():
    teams  = Team.objects.all()
    for team in teams:
        _, score = get_team_stats(team)
        Team.objects.filter(id=team.id).update(score=score)