from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

import logging

from .forms import RegisterForm, VitrineForm, ProdutoForm, PerfilForm, EncomendaForm
from .models import Vitrine, Produto, Perfil, Encomenda, Avaliacao

logger = logging.getLogger(__name__)

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
        showcase_exist = True
        return render(request, 'blog/produtoRegister.html', {'form': form, 'showcase_exist': showcase_exist})

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

def home_vitrineFilters(request, filter):
    needSearchCity = True
    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    elif filter == 'mais-acessos':
        try:
            vitrines = (Vitrine.objects.filter()).order_by('-acessos')
            logger.info('vitrines filtradas por numero de acessos')
            for v in vitrines:
                logger.debug(v.nome)
                logger.debug(v.acessos)
        except:
            logger.warning('Houve um problema na filtragem das vitrines')
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity,'vitrines': vitrines})

def home_category(request,category):
    needSearchCity = True
    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    else:
        vitrines = Vitrine.objects.filter(categoria = category)
        logger.info('categoria de vitrines selecionada')
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity,'vitrines': vitrines})

def home_page(request):
    needSearchCity = True
    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    else:
        vitrines = Vitrine.objects.filter()
    if request.user.is_authenticated:
        needSearchCity = False
    return render(request, 'blog/home.html', {'needSearchCity': needSearchCity, 'vitrines': vitrines})

@login_required
def perfil_cliente(request):
    perfil = Perfil.objects.filter(usuario=request.user)
    if perfil:
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            encomendas = Encomenda.objects.filter(cliente=request.user)
            return render(request, 'blog/perfilCliente.html', {'perfil': perfil, 'encomendas': encomendas})
        except:
            logger.warning('Houve um problema para passar o perfil ou encomendas para o template de perfil')
    return render(request, 'blog/perfilCliente.html', {'perfil': perfil})

def vitrine_home_client(request, pk):
    user_on = False
    vitrine = get_object_or_404(Vitrine, pk=pk)
    produtos = Produto.objects.filter(proprietario=vitrine)
    avaliacao = Avaliacao.objects.get_or_create(vitrine=vitrine)[0]
    if request.POST.get('rating'):
        if request.user.is_authenticated:
            calculateRatingStore(vitrine, request.POST.get('rating'), avaliacao, request.user)
    else:
        vitrine.acessos += 1
        vitrine.save()
        logger.info('Cliente acessou uma vitrine')
    if request.user.is_authenticated:
        user_on = True
    context = {'vitrine': vitrine, 'produtos': produtos, 'avaliacao': avaliacao, 'user_on': user_on}
    return render(request, 'blog/vitrineHomeClient.html', context)

@login_required
def vitrine_home_seller(request):
    user = request.user
    vitrine = Vitrine.objects.filter(proprietario=user)
    if not vitrine:
        return render(request, 'blog/vitrineHomeSeller.html')
    else:
        showcase_exist = True
        vitrine = Vitrine.objects.get(proprietario=user)
        produtos = Produto.objects.filter(proprietario=vitrine)
        return render(request, 'blog/vitrineHomeSeller.html', {'showcase_exist': showcase_exist,
        'vitrine': vitrine, 'produtos': produtos })

@login_required
def vitrine_management(request):
    showcase_exist = True
    vitrine = Vitrine.objects.get(proprietario=request.user)
    produtos = Produto.objects.filter(proprietario=vitrine)
    encomendas = Encomenda.objects.filter(vendedor=vitrine)
    return render(request, 'blog/vitrineManagementHome.html', {'produtos': produtos, 'encomendas': encomendas,
     'showcase_exist': showcase_exist })

def searchNameStore(request):
    try:
        logger.info('busca realizada de nome da loja na home')
        vitrines = Vitrine.objects.filter(nome = request.GET['name_store'])
        return vitrines
    except:
        logger.warning('Houve um problema na busca de uma loja na home')
        return ''

def calculateRatingStore(vitrine,rating, avaliacao, user_logado):
    logger.info(avaliacao)
    try:
        avaliacao.quantidade += 1
        logger.info('quantidade total de avaliacoes: {}'.format(avaliacao.quantidade))
        logger.info('média de avaliação: {}'.format(avaliacao.media_nota))
        logger.info('avaliacao do usuario: {}'.format(int(rating)))
        avaliacao.somaTotal_nota = int(avaliacao.somaTotal_nota + int(rating))
        logger.info('soma das notas: {}'.format((avaliacao.somaTotal_nota + int(rating))))
        new_rating = int(avaliacao.somaTotal_nota / avaliacao.quantidade)
        logger.info('nota: {}'.format(new_rating))
        avaliacao.media_nota = new_rating
        avaliacao.save()
        logger.info('Nova media de avaliacao: {}'.format(avaliacao.media_nota))
    except:
        logger.warning('Houve algum problema na avaliacao da vitrine')
