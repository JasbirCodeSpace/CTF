from django.contrib.auth.models import User
from teams.forms.team import TeamCaptainForm, TeamModelForm
from accounts.models.profile import Profile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from teams.forms import TeamRegister, TeamJoin
from teams.models import Team
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from teams.checks import is_team_captain
from django.contrib import messages
from django.views.generic.edit import DeleteView
from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalUpdateView,
  BSModalReadView,
  BSModalDeleteView
)

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

# class TeamUpdateView(BSModalUpdateView):
#     model = Team
#     template_name = 'teams/team-update.html'
#     form_class = TeamModelForm
#     success_message = 'Success: Team details updated successfully'
#     def get_success_url(self):
#         return reverse('team-view', args=[self.object.team_name])

@require_http_methods(["GET", "POST"])
@login_required
def team_update(request, pk):
    if not is_team_captain(request.user, pk):
        raise PermissionDenied()
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TeamModelForm(instance = team, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect(team)
        return redirect(team)
    else:
        form = TeamModelForm(instance=team)
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
        print('here')
        team.delete()
        return redirect('challenges')
    return render(request, 'teams/modals/team-delete.html', {'instance': team})