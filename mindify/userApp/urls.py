from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup-login', views.signInSignOutView, name='signup_login'),
    path('logout', views.signInSignOutView, name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profileEdit, name='profile_edit'),
    path('profile/change-password', views.changePassword, name='change_password'),
    path('profile/change-email', views.changeEmail, name='change_email'),
    path('profile/change-username', views.changeUsername, name='change_username'),
    path('profile/delete-user', views.deleteUser, name='delete_user'),
]
