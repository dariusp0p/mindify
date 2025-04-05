from django.shortcuts import render

def landing(request):
    return render(request, 'coreApp/landing.html')

def events(request):
    return render(request, 'coreApp/events.html')

def premium(request):
    return render(request, 'coreApp/premium.html')