from teams.models import Team

def is_team_captain(user, team_pk):
    team = Team.objects.filter(pk = team_pk).first()
    if team:
        if user.profile.team == team:
            return True
    return False
