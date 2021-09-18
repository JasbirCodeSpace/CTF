from challenges.models.challenge import Challenge
from django.db import models
from django.utils import timezone
from challenges.models import Challenge
from accounts.models import Profile

class Submission(models.Model):

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solves')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='submissions')
    timestamp = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return "{} solved {} at {}".format(self.user, self.challenge, self.timestamp)