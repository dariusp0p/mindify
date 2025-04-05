from django.shortcuts import render

def signup_login(request):
    return render(request, 'userApp/signup-login.html')

