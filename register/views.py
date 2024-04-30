from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from register.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


@csrf_protect
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": form})


# @csrf_protect
# def register_user(request):
#     with transaction.atomic():
#         if request.method == "POST":
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 # login(request, user)
#                 profile, created = Profile.objects.get_or_create(user=user,
#                                                                  defaults={'currency': form.cleaned_data['currency']})
#             if created:
#                 messages.success(request, "Registration successful and profile created.")
#             else:
#                 messages.info(request, "Registration successful but profile already existed.")
#                 return redirect("login")
#                 # messages.success(request, "Registration successful.")
#                 # return HttpResponse("Homepage")
#             messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = RegisterForm()
#     return render(request, "register/register.html", {"register_user": form})

@csrf_protect
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                messages.success(request, "Registration successful.")
                return redirect("login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"register_user": form})


@csrf_protect
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")
