from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vitrine, Produto, Perfil, Encomenda

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
    	model = User
    	fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Submit', 'Cadastrar'))

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('foto','cidade', 'estado', 'bairro', 'rua', 'numero', 'cep', 'ponto_referencia')

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Criar perfil'))

class VitrineForm(forms.ModelForm):

    class Meta:
        model = Vitrine
        fields = ('foto','nome', 'cidade', 'categoria','descricao')

class ProdutoForm(forms.ModelForm):
    valor = forms.DecimalField(min_value =0.01)

    class  Meta:
        model = Produto
        fields = ('foto','nome', 'categoria', 'valor','quantidade','data_criacao','descricao')

class EncomendaForm(forms.ModelForm):

    class Meta:
        model = Encomenda
        fields = ('quantidade', 'data_entrega', 'comentario')
