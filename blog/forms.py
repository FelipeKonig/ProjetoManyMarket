from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vitrine

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
    	model = User
    	fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class VitrineForm(forms.ModelForm):

    class Meta:
        model = Vitrine
        fields = ('nome', 'cidade', 'categoria',)

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ('name','user_name','password', 'email','age','sex','city')
