from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teams.models import Team
from django.db.models import Subquery, OuterRef, F, Max, Q
from django.db.models import OuterRef, Subquery

def hackerboard(request):
    set_team_scores()
    model_max_set = Team.objects.values('college_name').annotate(max_score=Max('score')).order_by()

    q_statement = Q()
    for pair in model_max_set:
        q_statement |= (Q(college_name__exact=pair['college_name']) & Q(score=pair['max_score']))

    teams = Team.objects.filter(q_statement)

    # top_teams_per_college = Team.objects.filter(
    #                                     college_name=OuterRef('college_name')
    #                                 ).order_by('-score')[:1]
    # teams = Team.objects.filter(
    #         id__in=Subquery(top_teams_per_college.values('id'))
    #     )
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