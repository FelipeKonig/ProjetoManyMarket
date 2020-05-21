from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm
# from .forms import UserForm
# from .models import User

# Create your views here.
def register(request):
    register = False
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            register = True
            form.save()
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form, 'register': register})

def home_page(request):
    needSearchCity = True
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity})

# def register_user(request):
#     form = UserForm(request.POST)
#     register = False
#     if form.is_valid():
#         user = form.save()
#         register = True
#     return render(request, 'blog/register.html', {'form': form, 'register': register, 'needSearchCity': False})
