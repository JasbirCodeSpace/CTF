from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    team_leader = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return "Team[ "+self.team_name+" ]"
    
    def get_absolute_url(self):
        return reverse("team-view", kwargs={"teamname": self.team_name})
    