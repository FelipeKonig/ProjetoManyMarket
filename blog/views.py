from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, VitrineForm, ProdutoForm
from .models import Vitrine, Produto

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

@login_required
def vitrine_register(request):
    register = False
    if request.method == "POST":
        form = VitrineForm(request.POST)
        if form.is_valid():
            register = True
            vitrine = form.save(commit=False)
            vitrine.proprietario = request.user
            vitrine.save()
            return redirect('vitrine_home_seller')
    else:
        form = VitrineForm()
    return render(request, 'blog/vitrineRegister.html', {'form': form})

@login_required
def produto_register(request):
        register = False
        if request.method == "POST":
            form = ProdutoForm(request.POST)
            if form.is_valid():
                register = True
                produto = form.save(commit=False)
                vitrine = get_object_or_404(Vitrine, proprietario= request.user)
                produto.proprietario = vitrine
                produto.save()
        else:
            form = ProdutoForm()
        return render(request, 'blog/produtoRegister.html', {'form': form, 'register': register})

def home_page(request):
    needSearchCity = True
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity})

@login_required
def vitrine_home_seller(request):
    showcase_exist = False
    user = request.user
    vitrine = Vitrine.objects.filter(proprietario=user)
    if not vitrine:
        return render(request, 'blog/vitrineHomeSeller.html', {'showcase_exist': showcase_exist})
    else:
        showcase_exist = True
        vitrine = get_object_or_404(Vitrine, proprietario=user)
        produtos = Produto.objects.filter(proprietario=vitrine)
        return render(request, 'blog/vitrineHomeSeller.html', {'showcase_exist': showcase_exist,
        'vitrine': vitrine, 'produtos': produtos })

@login_required
def vitrine_management(request):
    user = request.user
    vitrine = Vitrine.objects.filter(proprietario=user)
    vitrine = get_object_or_404(Vitrine, proprietario=user)
    produtos = Produto.objects.filter(proprietario=vitrine)
    return render(request, 'blog/vitrineManagementHome.html', {'produtos': produtos })

# def register_user(request):
#     form = UserForm(request.POST)
#     register = False
#     if form.is_valid():
#         user = form.save()
#         register = True
#     return render(request, 'blog/register.html', {'form': form, 'register': register, 'needSearchCity': False})
