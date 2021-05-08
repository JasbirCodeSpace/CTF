from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Thread(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"
        ordering = ("-date_created",)

    def __str__(self):
        return "{} created {} at {}".format(self.created_by.username, self.title, self.date_created)

    def get_absolute_url(self):
        return reverse("Thread_detail", kwargs={"pk": self.pk})
