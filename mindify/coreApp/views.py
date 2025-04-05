from django.shortcuts import render, redirect
from .models import User, Event, Tag
from django.forms.models import model_to_dict

def landing(request):
    user_id = request.session.get("user_id")

    user = None

    if user_id:
        user = User.objects.get(id=user_id)

    context = {
        "user": user
    } 

    return render(request, 'coreApp/landing.html', context)

def premium(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")
    
    user = User.objects.get(id=user_id)

    context = {
        "user": user
    }
    return render(request, 'coreApp/premium.html', context)

def events(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")
    
    user = User.objects.get(id=user_id)

    free_events = []

    for event in Event.objects.filter(id_creator=user.id, price=None):
        event_dict = model_to_dict(event)
        
        # Suprascriem doar ce vrei să fie prelucrat
        event_dict["title"] = event.title[:10]
        event_dict["date_posted"] = event.date_posted.date()

        free_events.append(event_dict)

    premium_events = []

    for event in Event.objects.filter(id_creator=user.id).exclude(price=None):
        event_dict = model_to_dict(event)
        
        # Suprascriem doar ce vrei să fie prelucrat
        event_dict["title"] = event.title[:10]
        event_dict["date_posted"] = event.date_posted.date()

        premium_events.append(event_dict)

    distinct_tags = Tag.objects.values_list('tag_name', flat=True).distinct()

    eventsFiltered = Event.objects.all()

    context = {
        "user": user,
        "freeEvents": free_events,
        "premiumEvents": premium_events,
        "tags": distinct_tags,
        "eventsFiltered": eventsFiltered,
    }
    
    return render(request, 'coreApp/events.html', context)