from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('events/', views.events, name='events'),
    path('premium/', views.premium, name='premium'),
]
