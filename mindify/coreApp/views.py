from django.shortcuts import render, redirect
from .models import User, Event, Tag
from django.forms.models import model_to_dict

# basic webite views
def homepage(request):
    user_id = request.session.get("user_id")

    user = None

    if user_id:
        user = User.objects.get(id=user_id)

    context = {
        "user": user
    } 

    return render(request, 'coreApp/homepage.html', context)

def about(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")
    
    user = User.objects.get(id=user_id)

    context = {
        "user": user
    }
    return render(request, 'coreApp/about.html')

def contact(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")
    
    user = User.objects.get(id=user_id)

    context = {
        "user": user
    }
    return render(request, 'coreApp/contact.html', context)

def premium(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")
    
    user = User.objects.get(id=user_id)

    context = {
        "user": user
    }
    return render(request, 'coreApp/premium.html', context)



# event feed
def mainpage(request):
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
    
    return render(request, 'coreApp/mainpage.html', context)


# event room
def room(request):
    return render(request, 'coreApp/room.html')





# event CRUD
def viewEvent(request):
    return render(request, 'coreApp/event/event-view.html')

def createEvent(request):
    return render(request, 'coreApp/event/event-create.html')

def editEvent(request):
    return render(request, 'coreApp/event/event-edit.html')

def deleteEvent(request):
    return render(request, 'coreApp/event/event-edit.html')


# payment views
def checkout(request):
    return render(request, 'coreApp/payment/payment-checkout.html')

def success(request):
    return render(request, 'coreApp/payment/payment-success.html')

    return render(request, 'coreApp/events.html', context)

from .models import Content
from .utilities import extract_text_from_file

def viewFileContent(request, content_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")

    user = User.objects.get(id=user_id)

    content = Content.objects.get(id=content_id)

    # Extragem textul din fișier
    file_path = content.file.path
    extracted_text = extract_text_from_file(file_path)

    context = {
        "user": user,
        "content": content,
        "extracted_text": extracted_text,
    }

    return render(request, 'coreApp/text_extraction_test.html', context)

# chatgpt
from .utils import chat_with_gpt
def ai_helper(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")

    user = User.objects.get(id=user_id)

    response = None

    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            response = chat_with_gpt(prompt)
            if not response:
                response = "Sorry, I couldn't process your request. Please try again."

    return render(request, 'coreApp/ai_helper.html', {'response': response, 'user': user})
