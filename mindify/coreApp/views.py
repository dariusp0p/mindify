from django.shortcuts import render

def landing(request):
    return render(request, 'coreApp/landing.html')

def events(request):
    return render(request, 'coreApp/events.html')

def premium(request):
    return render(request, 'coreApp/premium.html')

def createEvent(request):
    return render(request, 'coreApp/create-event.html')

def viewEvent(request):
    return render(request, 'coreApp/view-event.html')

def checkout(request):
    return render(request, 'coreApp/checkout.html')

def success(request):
    return render(request, 'coreApp/payment-success.html')