from django.db import models
from forum.models import Thread
from django.utils import timezone

class Answer(models.Model):

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    answer_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    date_created = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(default=timezone.now, auto_now=True, auto_now_add=False)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    accepted_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ("upvote", )

    def __str__(self):
        return "{} answered {} at {}".format(self.answer_by.username, self.answer, self.date_created)

    def get_absolute_url(self):
        return reverse("Answer_detail", kwargs={"pk": self.pk})
