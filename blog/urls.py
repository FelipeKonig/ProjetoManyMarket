from django.urls import path
from . import views

urlpatterns = [
    path('', views.basePage, name='base'),
    path('register', views.registerUser, name='registerUser'),
]
