from django.shortcuts import render, redirect
from .models import User, Event, Tag, Content
from django.forms.models import model_to_dict
from django.db.models import Q
import random
from .forms import CreateEventForm

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
    return render(request, 'coreApp/about.html', context)

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



# mainpage views
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

    context = {
        "user": user,
        "freeEvents": free_events,
        "premiumEvents": premium_events,
        "tags": distinct_tags,
    }

    #Extragerea filtrelor de cautare
    free_paid_filter = request.GET.getlist("type")
    selected_tags = request.GET.getlist("category")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    search = request.GET.get("searchBar")

    queryset = Event.objects.all()

    if free_paid_filter:
        price_filter = Q()
        if "Free" in free_paid_filter:
            price_filter |= Q(price__isnull=True) | Q(price=0)
        if "Paid" in free_paid_filter:
            price_filter |= Q(price__gt=0)
        queryset = queryset.filter(price_filter)

    # Filtru după taguri
    if selected_tags:
        queryset = queryset.filter(tags__tag_name__in=selected_tags)

    # # Filtru date
    if date_from and date_to:
        queryset = queryset.filter(date_posted__date__range=[date_from, date_to])
    elif date_from:
        queryset = queryset.filter(date_posted__date__gte=date_from)
    elif date_to:
        queryset = queryset.filter(date_posted__date__lte=date_to)
    
    #Search bar-ul
    if search:
        queryset = queryset.filter(title__icontains=search) #cauta un substring case insensitive in titles
    

    context = {
        **context, 
        **{
            "eventsFiltered": queryset,
            "selected_types": free_paid_filter,
            "selected_tags": selected_tags,
            "date_from": date_from,
            "date_to": date_to,
            "user": user,
        }
    } 

    subscribed_tags_queryset = Tag.objects.filter(event__subscription__id_user=user_id).distinct().values_list('tag_name', flat=True)

    # Get events that match the tags
    may_like_events = Event.objects.filter(tags__tag_name__in=subscribed_tags_queryset).distinct()

    # Convert to a list
    may_like_events = list(may_like_events)
    context = {
        **context,
        **{
            "recommandations": getRandomListOfRecommandations(may_like_events, 6),
        }
    }

    return render(request, 'coreApp/mainpage.html', context)


import random
def getRandomListOfRecommandations(events, numberOfEvents):
    if numberOfEvents > len(events):
        numberOfEvents = len(events)
    return random.sample(events, numberOfEvents) 

# event room
def room(request):
    return render(request, 'coreApp/room.html')



# event CRUD
def viewEvent(request):
    return render(request, 'coreApp/event/event-view.html')

def editEvent(request):
    return render(request, 'coreApp/event/event-edit.html')

def deleteEvent(request):
    return render(request, 'coreApp/event/event-edit.html')


# payment views
def checkout(request):
    return render(request, 'coreApp/payment/payment-checkout.html')

def success(request):
    return render(request, 'coreApp/payment/payment-success.html')

from django.shortcuts import render, redirect
from .forms import CreateEventForm
from coreApp.models import Event, Tag, Content

def createEvent(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup_login')

    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        print("msg1")
        if form.is_valid():
            print("msg2")
            # Extract form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            date_posted = form.cleaned_data['date_posted']
            event_picture = form.cleaned_data['event_picture']
            content_file = form.cleaned_data['content']
            price = form.cleaned_data['price']
            tags = form.cleaned_data['tags']  # Comma-separated string

            # Create and save the event
            event = Event.objects.create(
                id_creator_id=user_id,
                title=title,
                description=description,
                date_posted=date_posted,
                event_picture=event_picture,
                price=price,
            )

            # Save content associated with the event
            if content_file:
                Content.objects.create(
                    id_event=event,
                    file_saved=content_file,
                )

            # Process tags
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]  # Split by commas and strip whitespace
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                    event.tags.add(tag)  # Associate the tag with the event

            return redirect('main')  # Redirect to the event list page
    else:
        form = CreateEventForm()

    return render(request, 'coreApp/event/event-create.html', {'event_form': form})
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
