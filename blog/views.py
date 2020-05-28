from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, VitrineForm, ProdutoForm, PerfilForm
from .models import Vitrine, Produto, Perfil, Encomenda, Comentario

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, "registration/register.html", {"form":form})

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
        if request.method == "POST":
            form = ProdutoForm(request.POST)
            if form.is_valid():
                produto = form.save(commit=False)
                vitrine = Vitrine.objects.filter(proprietario=user)
                produto.proprietario = vitrine
                produto.save()
                return redirect('vitrine_home_seller')
        else:
            form = ProdutoForm()
        return render(request, 'blog/produtoRegister.html', {'form': form})

def perfil_register(request):
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            return redirect('home')
    else:
        form = PerfilForm()
    return render(request, "blog/perfilRegister.html", {"form":form})

def home_page(request):
    needSearchCity = True
    vitrines = Vitrine.objects.filter()
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity, 'vitrines': vitrines})

def vitrine_home_client(request, pk):
    vitrine = get_object_or_404(Vitrine, pk=pk)
    produtos = Produto.objects.filter(proprietario=vitrine)
    return render(request, 'blog/vitrineHomeClient.html', {'vitrine': vitrine, 'produtos': produtos})

@login_required
def vitrine_home_seller(request):
    showcase_exist = False
    user = request.user
    vitrine = Vitrine.objects.filter(proprietario=user)
    if not vitrine:
        return render(request, 'blog/vitrineHomeSeller.html', {'showcase_exist': showcase_exist})
    else:
        showcase_exist = True
        vitrine = Vitrine.objects.get(proprietario=user)
        produtos = Produto.objects.filter(proprietario=vitrine)
        return render(request, 'blog/vitrineHomeSeller.html', {'showcase_exist': showcase_exist,
        'vitrine': vitrine, 'produtos': produtos })

@login_required
def vitrine_management(request):
    user = request.user
    vitrine = Vitrine.objects.get(proprietario=user)
    produtos = Produto.objects.filter(proprietario=vitrine)
    return render(request, 'blog/vitrineManagementHome.html', {'produtos': produtos })

# def register_user(request):
#     form = UserForm(request.POST)
#     register = False
#     if form.is_valid():
#         user = form.save()
#         register = True
#     return render(request, 'blog/register.html', {'form': form, 'register': register, 'needSearchCity': False})
