from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vitrine, Produto, Perfil, Encomenda, Comentario

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
    	model = User
    	fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('cidade', 'estado')

class VitrineForm(forms.ModelForm):

    class Meta:
        model = Vitrine
        fields = ('nome', 'cidade', 'categoria','descricao')

class ProdutoForm(forms.ModelForm):
    valor = forms.DecimalField(min_value =0.01)

    class  Meta:
        model = Produto
        fields = ('nome', 'categoria', 'valor','quantidade','data_criacao','descricao')
