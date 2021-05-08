from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender =models.CharField(choices = GENDER_CHOICES, max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return "Profile[ "+self.user.username+" ]"