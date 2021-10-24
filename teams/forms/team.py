from django import forms;
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import fields
from teams.models.team import Team
from bootstrap_modal_forms.forms import BSModalModelForm
from django.shortcuts import get_object_or_404

class TeamRegister(forms.ModelForm):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team name'}), max_length=50, required=True, help_text="Enter team name")
    college_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'College name', 'readonly':'readonly'}), max_length=50, required=True, help_text="Enter college name")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Team password'}), max_length=50, required=True, help_text="Enter team password")

    class Meta:
        model = Team
        fields = ('team_name', 'college_name', 'password')
    
    def clean_team_name(self):
        team_name = self.cleaned_data['team_name']
        if Team.objects.filter(team_name = team_name).exists():
            raise forms.ValidationError("Team with this name already exist")
        return team_name
    
    
    def clean(self):
        cleaned_data = super(TeamRegister, self).clean()
        return cleaned_data
    
class TeamJoin(forms.Form):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team name'}), max_length=50, required=True, help_text="Enter team name")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Team password'}), max_length=50, required=True, help_text="Enter team password")

    
    def clean(self):
        cleaned_data = super(TeamJoin, self).clean()
        team_name = cleaned_data['team_name']
        password = cleaned_data['password']
        team = Team.objects.filter(team_name = team_name, password = password)

        if not team:
            raise forms.ValidationError("Invalid team name or password")

        if team.first().users.all().count()>=5:

            raise forms.ValidationError("Maximum 5 members allowed per team.")
 
        return cleaned_data


class TeamUpdateForm(forms.ModelForm):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team name'}), max_length=50, required=True, help_text="Enter team name")
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team password'}), max_length=50, required=True, help_text="Enter team password")

    class Meta:
        model = Team
        fields= ['team_name', 'password']
    
    # def clean_team_name(self):
    #     team_name = self.cleaned_data['team_name']
    #     print(self)
    #     if Team.objects.filter(team_name = team_name).exists():
    #         raise forms.ValidationError("Team with this name already exist")
    #     return team_name

class TeamCaptainForm(forms.Form):
    team_captain = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),empty_label=None)
    
    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id', None)
        super(TeamCaptainForm, self).__init__(*args, **kwargs)

        if team_id:
            team = get_object_or_404(Team, id=team_id)
            self.fields['team_captain'].queryset = team.users
            self.fields['team_captain'].label_from_instance = lambda obj: "%s" % obj.user.username

