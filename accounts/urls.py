from django import template
from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import profile
from .forms.profile import UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
urlpatterns = [
    path('register/', profile.profile_register, name='profile-register'),
    path('login/', profile.profile_login, name = 'profile-login'),
    path('logout/', profile.profile_logout, name='profile-logout'),
    path('view/<str:username>/', profile.profile_view, name='profile-view'),
    path('update/', profile.profile_update, name='profile-update'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', form_class=UserPasswordChangeForm), name='password_change'),
    path('change_password_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]