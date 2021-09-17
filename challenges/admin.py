from django.contrib import admin
from .models.category import Category
from .models.challenge import Challenge
from .models.submission import Submission

admin.site.register(Category)
admin.site.register(Challenge)
admin.site.register(Submission)

