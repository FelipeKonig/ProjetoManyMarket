from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm
from .models import User

def home_page(request):
    needSearchCity = True
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity})

def register_user(request):
    form = UserForm(request.POST)
    register = False
    if form.is_valid():
        user = form.save()
        register = True
    return render(request, 'blog/register.html', {'form': form, 'register': register, 'needSearchCity': False})
