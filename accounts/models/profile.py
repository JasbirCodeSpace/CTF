from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    age = models.IntegerField(null=True)
    gender =models.CharField(choices = GENDER_CHOICES, max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    team = models.ForeignKey("accounts.Team", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return "Profile[ "+self.user.username+" ]"
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user = instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user = instance)

        
    
        
    