from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('accounts/register/', views.register, name="register"),
    path('accounts/register/profile', views.perfil_register, name="register_perfil"),
    path('perfil', views.perfil_cliente, name="cliente_perfil"),
    path('vitrine/home/', views.vitrine_home_seller, name='vitrine_home_seller'),
    path('vitrine/cadastro', views.vitrine_register, name='vitrine_register'),
    path('vitrine/gerenciamento', views.vitrine_management, name='vitrine_management'),
    path('vitrine/cadastro/produto', views.produto_register, name='produto_register'),
    path('vitrine/vitrine/<int:pk>/', views.vitrine_home_client, name='vitrine_home_client')
    # path('register', views.register_user, name='register_user'),
]
