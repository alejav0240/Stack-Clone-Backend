from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    min_points = models.IntegerField()

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    # Solo agregas campos nuevos
    age = models.IntegerField(null=True, blank=True)
    rol = models.CharField(max_length=50 , default='user')
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rank = models.ForeignKey(Rank, null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()
    # Opcionalmente puedes cambiar cómo se ve el usuario
    def __str__(self):
        return self.username
