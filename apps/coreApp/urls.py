from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('premium/', views.premium, name='premium'),

    path('main/', views.mainpage, name='main'),
    path('main/room/', views.room, name='room'),

    path('event/view/', views.viewEvent, name='event_view'),
    path('event/create/', views.createEvent, name='event_create'),
    path('event/edit/<str:pk>', views.editEvent, name='event_edit'),
    path('event/delete/', views.deleteEvent, name='event_delete'),

    path('payment/checkout/', views.checkout, name='payment_checkout'),
    path('payment/success/', views.success, name='payment_success'),
    path('ai-helper/', views.ai_helper, name='ai_helper'),
    path('extract-text/<int:content_id>/', views.viewFileContent, name='extract_text'),
]
