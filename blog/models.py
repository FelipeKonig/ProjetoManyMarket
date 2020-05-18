from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class User(models.Model):

    sex_choices = (
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino"),
        ("N", "Nenhuma das opções")
    )
    name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=200, default='')
    age = models.PositiveSmallIntegerField()
    sex = models.CharField(choices=sex_choices, max_length=10, default='')

    def _str_(self):
        return self.name
