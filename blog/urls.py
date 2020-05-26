from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('accounts/register/', views.register, name="register"),
    path('vitrine', views.vitrine_home_seller, name='vitrine_home_seller'),
    path('vitrine/registro', views.vitrine_register, name='vitrine_register'),
    path('vitrine/gerenciamento', views.vitrine_management, name='vitrine_management')
    # path('register', views.register_user, name='register_user'),
]
