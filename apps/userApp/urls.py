from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup-login/', views.signupLogin, name='signup_login'),
    path('logout/', views.logout, name='logout'),

    path('', views.user, name='user'),
    path('edit/', views.editUser, name='edit_user'),
    path('change-email/', views.changeEmail, name='change_email'),
    path('change-username/', views.changeUsername, name='change_username'),
    path('change-password/', views.changePassword, name='change_password'),
    path('delete-user/', views.deleteUser, name='delete_user'),

    path('settings/', views.settings, name='settings'),
]
