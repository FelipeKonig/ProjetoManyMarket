from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('categoria/<str:category>', views.home_category, name='home_category'),
    path('categoria/<str:category>/<str:filter>/', views.home_vitrineFilters, name='home_vitrineFilters'),
    path('accounts/register/', views.register, name="register"),
    path('accounts/register/profile', views.perfil_register, name="register_perfil"),
    path('perfil', views.perfil_cliente, name="cliente_perfil"),
    path('vitrine/home/', views.vitrine_home_seller, name='vitrine_home_seller'),
    path('vitrine/home/<int:pk>/<str:category>/', views.vitrine_home_seller_category, name='vitrine_home_seller_category'),
    path('vitrine/cadastro', views.vitrine_register, name='vitrine_register'),
    path('vitrine/gerenciamento', views.vitrine_management, name='vitrine_management'),
    path('vitrine/cadastro/produto', views.produto_register, name='produto_register'),
    path('vitrine/<int:pk_vitrine>/produto/<int:pk_produto>/encomenda', views.encomendar_produto, name='produto_encomenda'),
    path('vitrine/<int:pk_vitrine>/<str:filter>/', views.vitrine_home_client_produtoFilter, name='vitrine_home_client_produtoFilters'),
    path('vitrine/<int:pk>/', views.vitrine_home_client, name='vitrine_home_client'),
    path('ajax/avaliacao/', views.avaliacao_vitrine, name='avaliacao_vitrine')
]
