from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

from .forms import SignUpForm, LoginForm
from coreApp.models import User

def signInSignOutView(request):
    if request.method == "POST":
        if 'login' in request.POST:
            logInForm = LoginForm(request.POST)

            if logInForm.is_valid():
                email = logInForm.cleaned_data['email']
                password = logInForm.cleaned_data['password']

                user = User.objects.filter(email=email).first()
                if user and password == user.password:
                    request.session['user_id'] = user.id
                    user.save()
                    return redirect('events')
                else:
                    print("Email sau parolă incorectă")
        elif 'signup' in request.POST:
            signUpForm = SignUpForm(request.POST)

            if signUpForm.is_valid():
                username = signUpForm.cleaned_data['username']
                email = signUpForm.cleaned_data['email']
                password = signUpForm.cleaned_data['password']

                user = User.objects.filter(email=email).first()
                if not user:
                    user = User.objects.create(username=username, email=email, password=password)
                    request.session['user_id'] = user.id
                    user.save()
                    return redirect('events')
                else:
                    print("User existent!")

    logInForm = LoginForm()
    signUpForm = SignUpForm()

    context = {
        'logInForm': logInForm,
        'signUpForm': signUpForm,
    }
    return render(request, 'userApp/signup-login.html', context)


def logoutView(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("landing")

    user = User.objects.get(id=user_id)

    user.active_now = False
    user.save()
    update_last_online(request)
    request.session.pop("user_id")
    return redirect('landing')


@csrf_exempt
def update_last_online(request):
    """Actualizează last_time_online la ieșirea utilizatorului"""
    user_id = request.session.get('user_id')

    if not user_id:  # Dacă sesiunea nu există, nu face nimic
        return JsonResponse({"status": "session expired"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.last_login = datetime.datetime.now()
        user.save()
        return JsonResponse({"status": "success"})
    except User.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)