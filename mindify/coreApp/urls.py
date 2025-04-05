from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('events/', views.events, name='events'),
    path('premium/', views.premium, name='premium'),
    path('events/create', views.createEvent, name='create_event'),
    path('events/view', views.viewEvent, name='view_event'),
    path('events/checkout', views.checkout, name='checkout'),
    path('payment/success', views.success, name='success'),
]
