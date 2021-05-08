from django.db import models
from django.utils import timezone

class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50, unique=True)
    score = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=False)
    updated_time = models.TimeField(default=timezone.now, auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return "Team[ "+self.team_name+" ]"