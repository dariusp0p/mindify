from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup-login/', views.signInSignOutView, name='signup_login'),
    path('logout/', views.logoutView, name='logout'),
]
