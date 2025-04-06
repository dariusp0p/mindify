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
                    user.is_active = True
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
                    user.is_active = True
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
        return redirect('signup_login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup_login')
    date_joined = user.date_joined.strftime('%d.%m.%Y') if user and user.date_joined else None

    you_are_part_of = Subscription.objects.filter(id_user=user_id, left_date=None).order_by('-joined_date')
    number_of_subscriptions_you_are_part_of = you_are_part_of.count()
    your_events = Event.objects.filter(id_creator=user_id).order_by('-date_posted')
    number_of_events = your_events.count()

    context = {
        'user': user,
        'date_joined': date_joined,
        'you_are_part_of': you_are_part_of,
        'your_events': your_events,
        'nrOfSubscriptions': number_of_subscriptions_you_are_part_of,
        'nrOfEvents': number_of_events,
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
        return redirect('signup_login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup_login')

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.gender = form.cleaned_data.get('gender', user.gender)
            if form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data['profile_picture']
            user.save()
            return redirect('user')
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

from .forms import ResetPasswordForm
def changePassword(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup_login')

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if user.password != old_password:
                return render(request, 'userApp/change-password.html', {'output': 'Parola veche este greșită', 'form': ResetPasswordForm()})
            
            if new_password != confirm_password:
                return render(request, 'userApp/change-password.html', {'output': 'Parolele nu se potrivesc', 'form': ResetPasswordForm()})

            user.password = new_password
            user.save()
            return redirect('user')
        
    form = ResetPasswordForm()
    return render(request, 'userApp/change-password.html', {'form': form})

from .forms import ChangeEmailForm
def changeEmail(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup-login')

    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=new_email).exists():
                return render(request, 'userApp/change-email.html', {'output': 'Email existent', 'form': ChangeEmailForm()})
            
            if user.password == password:
                user.email = new_email
                user.save()
                return redirect('user')
            
    form = ChangeEmailForm()
    return render(request, 'userApp/change-email.html', {'form': form})

from .forms import ChangeUsernameForm
def changeUsername(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup_login')

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            password = form.cleaned_data['password']
            
            if user.password == password:
                user.username = new_username
                user.save()
                return redirect('user')
            return render(request, 'userApp/change-username.html', {'output': 'Parola greșită', 'form': ChangeUsernameForm()})
            
    form = ChangeUsernameForm()
    return render(request, 'userApp/change-username.html', {'form': form})

from .forms import DeleteAccount
def deleteUser(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup_login')

    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = DeleteAccount(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if user.password == password:
                user.delete()
                request.session.pop('user_id')
                return redirect('signup_login')
            
    form = DeleteAccount()
    return render(request, 'userApp/delete-user.html', {'form': form})


def settings(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup_login')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('signup_login')

    context = {
        'user': user,
    }
    return render(request, 'userApp/settings.html', context)
