from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('accounts/register/', views.register, name="register"),
    path('vitrine', views.vitrine_home, name='vitrine_home'),
    path('vitrine/registro', views.vitrine_register, name='vitrine_register')
    # path('register', views.register_user, name='register_user'),
]
