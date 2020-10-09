from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages

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
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('home')
        else:
            messages.warning(request, 'Usuário não cadastrado')
    else:
        form = RegisterForm()
        return render(request, "registration/register.html", {"form":form})

@login_required
def vitrine_register(request):
    register = False
    if request.method == "POST":
        form = VitrineForm(request.POST, request.FILES)
        if form.is_valid():
            register = True
            vitrine = form.save(commit=False)
            vitrine.proprietario = request.user
            vitrine.save()
            messages.success(request, 'Vitrine registrada com sucesso')
            return redirect('vitrine_home_seller')
        else:
            messages.warning(request, 'Não foi possível registrar a vitrine')
    else:
        form = VitrineForm()
    return render(request, 'blog/vitrineRegister.html', {'form': form})

@login_required
def produto_register(request):
        if request.method == "POST":
            form = ProdutoForm(request.POST, request.FILES)
            if form.is_valid():
                produto = form.save(commit=False)
                vitrine = Vitrine.objects.get(proprietario=request.user)
                produto.proprietario = vitrine
                produto.save()
                messages.success(request, 'Produto registrado com sucesso')
                return redirect('vitrine_home_seller')
            else:
                messages.warning(request, 'Não foi possível cadastrar o produto')
        else:
            form = ProdutoForm()
        showcase_exist = True
        return render(request, 'blog/produtoRegister.html', {'form': form, 'showcase_exist': showcase_exist})

def perfil_register(request):
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, 'Perfil cadastrado com sucesso')
            return redirect('cliente_perfil')
        else:
            messages.warning(request, 'Não foi possível cadastrar o perfil')
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
            messages.success(request, 'Encomenda realizada com sucesso')
            return redirect('cliente_perfil')
        else:
            messages.warning(request, 'Não foi possível realizar a encomenda')
    else:
        form = EncomendaForm()
    return render(request, 'blog/produtoEncomenda.html', {
        "form":form, 'vitrine': vitrine, 'produto': produto, 'profile_exist': profile_exist
    })

def home_vitrineFilters(request, filter, category):
    needSearchCity = True
    vitrines = filterStoresHome(request,filter, category)
    if request.user.is_authenticated:
        needSearchCity = False
    context = {'needSearchCity': needSearchCity,'vitrines': vitrines, 'category': category}
    return render(request, 'blog/home.html', context)

def home_category(request,category):
    needSearchCity = True
    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    else:
        vitrines = Vitrine.objects.filter(categoria = category)
        logger.info('categoria de vitrines selecionada')
    if request.user.is_authenticated:
        needSearchCity = False
    context = {'needSearchCity': needSearchCity,'vitrines': vitrines, 'category': category}
    return render(request, 'blog/home.html', context)

def home_page(request):
    needSearchCity = True

    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    else:
        vitrines = Vitrine.objects.filter()
    if request.user.is_authenticated:
        needSearchCity = False
    context = {'needSearchCity': needSearchCity, 'vitrines': vitrines, 'category': 'geral'}
    return render(request, 'blog/home.html', context)

@login_required
def perfil_cliente(request):

    perfil = Perfil.objects.filter(usuario=request.user)

    if request.method == "POST":
        logger.info(' nova imagem de perfil: {}'.format(request.FILES.get('image')))
        try:
            perfil.foto = request.FILES.get('image')
            perfil.save()
            messages.sucess(request, 'Foto de perfil atualizada com sucesso')
            logger.info('foto de perfil atualizada')
        except:
            messages.warning(request, 'Não foi possível atualizar sua foto')
            logger.info('a foto de perfil não pode ser atualizada')
    if perfil:
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            encomendas = Encomenda.objects.filter(cliente=request.user)
            return render(request, 'blog/perfilCliente.html', {'perfil': perfil, 'encomendas': encomendas})
        except:
            logger.error('Houve um problema para passar o perfil ou encomendas para o template de perfil')
    return render(request, 'blog/perfilCliente.html', {'perfil': perfil})

def vitrine_home_client(request, pk):
    user_on = False

    vitrine = get_object_or_404(Vitrine, pk=pk)
    produtos = Produto.objects.filter(proprietario=vitrine)
    avaliacao = Avaliacao.objects.get_or_create(vitrine=vitrine)[0]

    if request.GET.get('name_product'):
        produtos = searchNameProductStore(request.GET.get('name_product'), vitrine)
    if request.POST.get('rating'):
        if request.user.is_authenticated:
            calculateRatingStore(vitrine, request.POST.get('rating'), avaliacao, request.user)
    else:
        vitrine.acessos += 1
        vitrine.save()
        logger.info('Cliente acessou uma vitrine')
    if request.user.is_authenticated:
        user_on = True
    context = {'vitrine': vitrine, 'produtos': produtos, 'avaliacao': avaliacao, 'user_on': user_on, 'filter': 'geral'}
    return render(request, 'blog/vitrineHomeClient.html', context)

def vitrine_home_client_produtoFilter(request, pk_vitrine, filter):
    user_on = False

    vitrine = get_object_or_404(Vitrine, pk=pk_vitrine)
    avaliacao = Avaliacao.objects.filter(vitrine=vitrine)[0]
    produtos = filterProductsStore(filter, vitrine)

    if request.GET.get('name_product'):
        produtos = searchNameProductStore(request.GET.get('name_product'), vitrine)

    if request.POST.get('rating'):
        if request.user.is_authenticated:
            calculateRatingStore(vitrine, request.POST.get('rating'), avaliacao, request.user)

    if request.user.is_authenticated:
        user_on = True

    context = {'vitrine': vitrine, 'produtos': produtos, 'user_on': user_on, 'avaliacao': avaliacao, 'filter': filter}
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
        avaliacao = Avaliacao.objects.filter(vitrine=vitrine)[0]
        produtos = Produto.objects.filter(proprietario=vitrine)
        context = {'showcase_exist': showcase_exist, 'vitrine': vitrine, 'produtos': produtos, 'avaliacao': avaliacao, 'category': 'geral'}
        return render(request, 'blog/vitrineHomeSeller.html', context)

def vitrine_home_seller_category(request, category, pk):
    try:
        vitrine = get_object_or_404(Vitrine, pk = pk)
        produtos = Produto.objects.filter(proprietario=vitrine, categoria__iexact=category)
        logger.info('A vitrine filtou seus produtos pela categoria {}'.format(category))
    except:
        logger.warning('Não foi possível a vitrine filtrar seus produtos')

    context = {'showcase_exist': True, 'vitrine': vitrine, 'produtos': produtos, 'category': category}
    return render(request, 'blog/vitrineHomeSeller.html', context)

@login_required
def vitrine_management(request):
    showcase_exist = True
    vitrine = Vitrine.objects.get(proprietario=request.user)
    produtos = Produto.objects.filter(proprietario=vitrine)
    encomendas = Encomenda.objects.filter(vendedor=vitrine)
    context = {'produtos': produtos, 'encomendas': encomendas,'showcase_exist': showcase_exist }
    return render(request, 'blog/vitrineManagementHome.html', context)

def searchNameStore(request):
    try:
        vitrines = Vitrine.objects.filter(nome__icontains = request.GET['name_store'])
        logger.info('busca por nome da loja realizada na home')
        return vitrines
    except:
        logger.warning('Houve um problema na busca de uma loja na home')
        return ''

def filterStoresHome(request, filter, category):
    if request.GET.get('name_store'):
        vitrines = searchNameStore(request)
    elif filter == 'mais-acessos':
        try:
            if category == 'geral':
                vitrines = (Vitrine.objects.filter()).order_by('-acessos')
            else:
                vitrines = (Vitrine.objects.filter(categoria__iexact=category)).order_by('-acessos')
            logger.info('vitrines filtradas por numero de acessos')
            for v in vitrines:
                logger.debug(v.nome)
                logger.debug(v.acessos)
        except:
            logger.warning('Houve um problema na filtragem das vitrines por mais acessos')
    elif filter == 'melhores-avaliacoes':
        try:
            if category == 'geral':
                vitrines = Vitrine.objects.order_by('-avaliacao__media_nota')
            else:
                vitrines = (Vitrine.objects.filter(categoria__iexact=category)).order_by('-avaliacao__media_nota')
            logger.info('vitrines filtradas por ordem de avaliacoes')
        except:
            logger.critical('Houve um problema na filtragem das vitrines por melhores avaliacoes')
    return vitrines

def filterProductsStore(request, vitrine):
    try:
        logger.info(request)
        if request == 'menor-preco':
            produtos = Produto.objects.filter(proprietario = vitrine).order_by('valor')

        elif request == 'maior-preco':
            produtos = Produto.objects.filter(proprietario = vitrine).order_by('-valor')

        logger.info('busca de produtos por filtro realizada na vitrine')
        return produtos
    except:
        logger.warning('Houve um problema na busca de um produto por filtro na vitrine')
        return ''

def searchNameProductStore(request, vitrine):
    try:
        produtos = Produto.objects.filter(nome__icontains = request, proprietario = vitrine)
        logger.info('busca de nome do produto realizada na vitrine')
        return produtos
    except:
        logger.warning('Houve um problema na busca de um produto por nome na vitrine')
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
