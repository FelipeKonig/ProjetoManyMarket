from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Vitrine(models.Model):

    categoria = (
        ("Informatica", "Informática"),
        ("Celulares", "Celulares"),
        ("Moda", "Moda")
    )
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=categoria)
    descricao = models.TextField(default='', null=True)

    def __str__(self):
        return self.nome
