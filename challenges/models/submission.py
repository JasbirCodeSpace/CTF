from django.db import models
from django.utils import timezone
from accounts.models import Team
from problems.models import Problem

class Submission(models.Model):

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return "{} solved {} at {}".format(self.team, self.problem, self.time)