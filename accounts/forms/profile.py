from django import forms;
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

class SignUpForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    )
    name = forms.CharField(max_length=50, required=True, help_text="Enter your name")
    email = forms.EmailField(max_length=254, required=True, help_text="Enter your email id")
    age = forms.IntegerField(required=True, help_text="Enter your age")
    gender =forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    state = forms.CharField(max_length=50, required=True, help_text="Enter your state name")
    country = forms.CharField(max_length=50, required=True, help_text="Enter your country name")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'email', 'age', 'gender', 'state', 'country')