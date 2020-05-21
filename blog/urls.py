from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path("accounts/register/", views.register, name="register"),
    # path('register', views.register_user, name='register_user'),
]
