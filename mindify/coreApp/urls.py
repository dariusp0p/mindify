from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('premium/', views.premium, name='premium'),
    path('main/', views.mainpage, name='mainpage'),

    path('main/room/', views.room, name='room'),

    path('event/view/', views.viewEvent, name='view_event'),
    path('event/create/', views.createEvent, name='create_event'),
    path('event/edit/', views.editEvent, name='edit_event'),
    path('event/delete/', views.deleteEvent, name='delete_event'),

    path('payment/checkout/', views.checkout, name='payment_checkout'),
    path('payment/success/', views.success, name='payment_success'),
]
