from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from.models import Platillo

from .forms import SushiForm

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('sushi')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def home(request):
    return render(request, 'home.html')

    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('sushi')

def create_platillo(request):
    if request.method == 'GET':
        return render(request, 'create_platillo.html', {"form": SushiForm})
    else:
        try:
            form = SushiForm(request.POST)
            new_sushi = form.save(commit=False)
            new_sushi.user = request.user
            new_sushi.save()
            return redirect('sushi')
        except ValueError:
            return render(request, 'create_platillo.html', {"form": SushiForm, "error": "Error al agregar platillo."})

@login_required
def signout(request):
    logout(request)
    messages.success(request, "La sesión se ha cerrado correctamente")
    return redirect('home')

@login_required
def sushi(request):
    sushi_dishes = Platillo.objects.all()  # Obtiene todos los platillos de sushi
    return render(request, 'sushi.html', {"sushi_dishes": sushi_dishes})
