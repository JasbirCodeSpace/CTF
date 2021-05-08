from django.db import models
from django.utils import timezone

class Problem(models.Model):

    CATEGORIES = (
        (1, "WEB"),
        (2, "REV"),
        (3, "CRYPTO"),
    )
    
    title = models.CharField(max_length=50)
    decription = models.TextField()
    category = models.IntegerField(choices=CATEGORIES)
    hint = models.TextField()
    score = models.IntegerField()
    flag = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Problem"
        verbose_name_plural = "Problems"
        ordering = ('score', )

    def __str__(self):
        return "Problem[ "+self.title+" ]"
