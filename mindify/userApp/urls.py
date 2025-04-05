from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup-login', views.signup_login, name='signup_login'),
]
