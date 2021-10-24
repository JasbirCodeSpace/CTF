from django.contrib.auth.models import User
from django.http.request import QueryDict
from django.http.response import HttpResponse
from teams.forms.team import TeamCaptainForm, TeamUpdateForm
from accounts.models.profile import Profile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from teams.forms import TeamRegister, TeamJoin
from teams.models import Team
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from teams.checks import is_team_captain, is_team_member
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.hashers import check_password, make_password
import datetime
import json
from urllib.parse import parse_qs, quote_plus, urlencode

salt = "Y:[zTwN/z-[u2>{b"

@login_required(login_url='profile-login')
def team_create(request):
    if request.user.profile.team:
        return redirect('home')
    if request.method == 'POST':
        form = TeamRegister(data = request.POST)
        if form.is_valid():
            team = Team()
            team.team_name = form.cleaned_data['team_name']
            team.college_name = request.user.profile.college
            team.password = form.cleaned_data['password']
            team.team_leader = request.user
            team.save()

            profile  = Profile.objects.get(user = request.user)
            profile.team = team
            profile.save(update_fields=['team'])
            return redirect('home')
    else:
        form = TeamRegister(initial={'college_name':request.user.profile.college})
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
    invitation_code = None
    if request.user == team.team_leader:
        # salt = str(datetime.date.today())
        invitation_code=make_password(password=team.password, salt=salt)
    if not team:
        return render(request, 'teams/team-create.html')
    
    members, submissions, score = get_team_stats(team)

    return render(request, 'teams/team.html', {'team':team, 'score': score, 'members': members, 'submissions': submissions, 'invitation_code': invitation_code})

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


@require_http_methods(["GET", "POST"])
@login_required
def team_update(request, pk):
    if not is_team_captain(request.user, pk):
        raise PermissionDenied()
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TeamUpdateForm(request.POST or None, instance = team)

        if form.is_valid():
            form.save()
            return redirect(team)
        else:
            list(messages.get_messages(request))
            form_errors = json.loads(form.errors.as_json())
            for field in form_errors:
                for field_error in form_errors[field]:
                    messages.error(request, field_error['message'])
            return redirect(request.user.profile.team)
    else:
        form = TeamUpdateForm(instance=team)
        return render(request, 'teams/modals/team-update.html', {'form': form, 'instance': team})
    
    
@require_http_methods(["GET", "POST"])
@login_required
def team_captain_change(request, pk):
    if not is_team_captain(request.user, pk):
        raise PermissionDenied()
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TeamCaptainForm(request.POST)
        if form.is_valid():
            captain = form.cleaned_data.get('team_captain')
            profile = get_object_or_404(Profile, user = User.objects.get(username=captain))
            if profile in team.users.all():
                Team.objects.filter(id=pk).update(team_leader=profile.user)
            return redirect(team)
        return redirect(team)
    else:
        form = TeamCaptainForm(team_id=pk, initial={'team_captain': team.team_leader.id})
        return render(request, 'teams/modals/team-captain.html', {'form': form, 'instance': team})
    
@login_required
def team_delete(request, pk):
    if not is_team_captain(request.user, pk):
        raise PermissionDenied()
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        team.delete()
        return redirect('challenges')
    return render(request, 'teams/modals/team-delete.html', {'instance': team})

@login_required
def team_leave(request, pk):
    if not is_team_member(request.user, pk):
        raise PermissionDenied()
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        Profile.objects.filter(user=request.user).update(team=None)
        return redirect(request.user.profile)
    return render(request, 'teams/modals/team-leave.html', {'instance': team})

@login_required
def team_invite(request, teamname):
    team = get_object_or_404(Team, team_name = teamname)
    users_count = team.users.all().count()

    if users_count>=5:
        raise PermissionDenied("Maximum 5 members allowed per team.")

    invitation_code = request.GET['code'].replace(" ", "+")

    if check_password(team.password,invitation_code):
        if request.user.profile.team is not None and request.user.profile.team.team_leader == request.user:
            raise PermissionDenied("Disband your team before joining this team.")
        Profile.objects.filter(user=request.user).update(team = team)
        return redirect(team)
    else:
        raise PermissionDenied("Invalid team invitation link.")

@login_required
def team_choice(request):
    if request.user.profile.team is None:
        return render(request, 'teams/team-choice.html')
    else:
        return redirect(request.user.profile.team)

