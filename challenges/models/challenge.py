from challenges.models.category import Category
from datetime import time
from django.db import models
from django.utils import timezone
import hashlib

def get_upload_path(instance, filename):
    return instance.category.name+'/challenges_{0}/{1}'.format(hashlib.md5(instance.title.encode('utf-8')).hexdigest(), filename)

class Challenge(models.Model):
    CHALLENGE_DIFFICULTY = (
        (1, "EASY"),
        (2, "MEDIUM"),
        (3, "HARD"),
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.IntegerField(choices=CHALLENGE_DIFFICULTY)
    hint = models.TextField(null=True, blank=True)
    score = models.IntegerField()
    file = models.FileField(null=True, blank=True, upload_to=get_upload_path)
    flag = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    num_solves = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

    def __str__(self):
        return "Challenge[ "+self.title+" ]"