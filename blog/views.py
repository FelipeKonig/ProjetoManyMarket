from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm
from .models import User

def basePage(request):
    return render(request, 'blog/base.html')

def registerUser(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save()
    return render(request, 'blog/register.html', {'form': form})
