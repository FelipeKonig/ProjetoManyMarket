from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import RegisterForm, VitrineForm, ProdutoForm, PerfilForm, EncomendaForm
from .models import Vitrine, Produto, Perfil, Encomenda

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
                vitrine = Vitrine.objects.get(proprietario=request.user)
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
            return redirect('cliente_perfil')
    else:
        form = PerfilForm()
    return render(request, "blog/perfilRegister.html", {"form":form})

@login_required
def encomendar_produto(request, pk_vitrine, pk_produto):

    profile_exist = False
    perfil = Perfil.objects.filter(usuario=request.user)
    if perfil:
        profile_exist = True
    print(profile_exist)
    vitrine = get_object_or_404(Vitrine, pk = pk_vitrine)
    produto = get_object_or_404(Produto, pk = pk_produto)
    if request.method == "POST":
        form = EncomendaForm(request.POST)
        if form.is_valid():
            encomenda = form.save(commit=False)
            encomenda.vendedor = vitrine
            encomenda.cliente = request.user
            encomenda.produto = produto
            encomenda.data_pedido = timezone.now()
            encomenda.save()
            return redirect('cliente_perfil')
    else:
        form = EncomendaForm()
    return render(request, 'blog/produtoEncomenda.html', {
        "form":form, 'vitrine': vitrine, 'produto': produto, 'profile_exist': profile_exist
    })

def home_page(request):
    needSearchCity = True
    vitrines = Vitrine.objects.filter()
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity, 'vitrines': vitrines})

@login_required
def perfil_cliente(request):
    perfil = Perfil.objects.filter(usuario=request.user)
    if perfil:
        perfil = Perfil.objects.get(usuario=request.user)
        encomendas = Encomenda.objects.filter(cliente=request.user)
        return render(request, 'blog/perfilCliente.html', {'perfil': perfil, 'encomendas': encomendas})
    return render(request, 'blog/perfilCliente.html', {'perfil': perfil})

def vitrine_home_client(request, pk):
    user_on = False
    vitrine = get_object_or_404(Vitrine, pk=pk)
    produtos = Produto.objects.filter(proprietario=vitrine)
    if request.user.is_authenticated:
        user_on = True
    return render(request, 'blog/vitrineHomeClient.html', {'vitrine': vitrine, 'produtos': produtos, 'user_on': user_on})

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
    vitrine = Vitrine.objects.get(proprietario=request.user)
    produtos = Produto.objects.filter(proprietario=vitrine)
    encomendas = Encomenda.objects.filter(vendedor=vitrine)
    return render(request, 'blog/vitrineManagementHome.html', {'produtos': produtos, 'encomendas': encomendas })
