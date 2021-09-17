from django import forms;
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import fields
from accounts.models.profile import Profile

class RegisterForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    )
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),required=True, help_text="Enter username")
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),min_length=8,required=True, help_text="Enter password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}),min_length=8,required=True, help_text="Reenter password")
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),max_length=50, required=True, help_text="Enter your name")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),max_length=254, required=True, help_text="Enter your email id")
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Age'}),required=True, help_text="Enter your age")
    gender =forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Gender'}),choices=GENDER_CHOICES, required=True)
    # state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),max_length=50, required=True, help_text="Enter your state name")
    # country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),max_length=50, required=True, help_text="Enter your country name")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'email', 'age', 'gender')
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Account with this email already exist.")
        return email
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ('user','team', 'score',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full name'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'age':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Age'}),
            'gender':forms.Select(attrs={'class':'form-control', 'placeholder':'Gender'}),
            # 'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
            # 'country':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),
        }

class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),required=True, help_text="Enter username")
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),required=True, help_text="Enter password")
    class Meta:
        model = User
        fields = ('username', 'password')

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
    
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
        'type': 'email',
        'name': 'email'
        }))
class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype password'}))

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype new password'}))

