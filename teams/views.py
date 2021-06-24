from accounts.models.profile import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teams.forms import TeamRegister, TeamJoin
from teams.models import Team

@login_required(login_url='profile-login')
def team_create(request):
    if request.user.profile.team:
        return redirect('home')
    if request.method == 'POST':
        form = TeamRegister(data = request.POST)
        if form.is_valid():
            team = Team()
            team.team_name = form.cleaned_data['team_name']
            team.college_name = form.cleaned_data['college_name']
            team.password = form.cleaned_data['password']
            team.team_leader = request.user
            team.save()

            profile  = Profile.objects.get(user = request.user)
            profile.team = team
            profile.save(update_fields=['team'])
            return redirect('home')
    else:
        form = TeamRegister()
    return render(request, 'teams/team-create.html', {'form':form})

@login_required(login_url='profile-login')
def team_join(request):
    if request.user.profile.team:
        return redirect('home')
    if request.method == 'POST':
        form = TeamJoin(data = request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            password = form.cleaned_data['password']
            team = Team.objects.get(team_name = team_name, password = password)
            profile  = Profile.objects.get(user = request.user)
            profile.team = team
            profile.save(update_fields=['team'])
            return redirect('home')
    else:
        form = TeamRegister()
    return render(request, 'teams/team-join.html', {'form':form}) 

@login_required
def team_view(request, teamname):
    team = Team.objects.get(team_name = teamname)
    if not team:
        return render(request, 'teams/team-create.html')
    
    members, submissions, score = get_team_stats(team)

    return render(request, 'teams/team.html', {'team':team, 'score': score, 'members': members, 'submissions': submissions})

def get_team_stats(team):
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
    for challenge, submission in team_submissions.items():
        team_score += challenge.score
        submissions.append(submission)
    
    return users,submissions, team_score