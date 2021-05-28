from django.contrib import admin
from .models.profile import Profile
from .models.team import Team

admin.site.register(Profile)
admin.site.register(Team)
