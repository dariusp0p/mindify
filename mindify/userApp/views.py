from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

from .forms import SignUpForm, LoginForm
from coreApp.models import User

from coreApp.models import Subscription, Event

# signup-login-logout views
def signupLogin(request):
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
                    return redirect('main')
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
                    return redirect('main')
                else:
                    print("User existent!")

    logInForm = LoginForm()
    signUpForm = SignUpForm()

    context = {
        'logInForm': logInForm,
        'signUpForm': signUpForm,
    }
    return render(request, 'userApp/signup-login.html', context)


def logout(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("homepage")

    user = User.objects.get(id=user_id)

    user.active_now = False
    user.save()
    update_last_online(request)
    request.session.pop("user_id")
    return redirect('homepage')




# profile views
def user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup-login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup-login')
    date_joined = user.date_joined.strftime('%d.%m.%Y') if user and user.date_joined else None

    you_are_part_of = Subscription.objects.filter(id_user=user_id, left_date=None).order_by('-joined_date')
    your_events = Event.objects.filter(id_creator=user_id).order_by('-date_posted')

    context = {
        'user': user,
        'date_joined': date_joined,
        'you_are_part_of': you_are_part_of,
        'your_events': your_events,
    }
    return render(request, 'userApp/user.html', context)

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


from .forms import ProfileEditForm
def editUser(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup-login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup-login')

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.gender = form.cleaned_data.get('gender', user.gender)
            if form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data['profile_picture']
            user.save()
            return redirect('profile')
    else:
       
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'profile_picture': user.profile_picture,
        }
        form = ProfileEditForm(initial=initial_data)
        context = {
            'form': form,
            'pfp': user.profile_picture.url if user.profile_picture else None,
        }

    return render(request, 'userApp/edit-user.html', context)

def changePassword(request):
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     return redirect('signup-login')

    # user = User.objects.get(id=user_id)

    # if request.method == "POST":
    #     new_password = request.POST.get('new_password')
    #     user.password = new_password
    #     user.save()
    #     return redirect('profile')

    # context = {
    #     'user': user,
    # }
    return render(request, 'userApp/change-password.html')

def changeEmail(request):
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     return redirect('signup-login')

    # user = User.objects.get(id=user_id)

    # if request.method == "POST":
    #     new_email = request.POST.get('new_email')
    #     user.email = new_email
    #     user.save()
    #     return redirect('profile')

    # context = {
    #     'user': user,
    # }
    return render(request, 'userApp/change-email.html')

def changeUsername(request):
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     return redirect('signup-login')

    # user = User.objects.get(id=user_id)

    # if request.method == "POST":
    #     new_username = request.POST.get('new_username')
    #     user.username = new_username
    #     user.save()
    #     return redirect('profile')

    # context = {
    #     'user': user,
    # }
    return render(request, 'userApp/change-username.html')

def deleteUser(request):
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     return redirect('signup-login')

    # user = User.objects.get(id=user_id)

    # if request.method == "POST":
    #     user.delete()
    #     return redirect('signup-login')

    # context = {
    #     'user': user,
    # }
    return render(request, 'userApp/delete-user.html')


def settings(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup-login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup-login')

    context = {
        'user': user,
    }
    return render(request, 'userApp/settings.html', context)