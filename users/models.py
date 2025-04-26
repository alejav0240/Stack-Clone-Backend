from django.contrib.auth.models import AbstractUser
from django.db import models

class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    min_points = models.IntegerField()

class CustomUser(AbstractUser):
    # Solo agregas campos nuevos
    age = models.IntegerField(null=True, blank=True)
    rol = models.CharField(max_length=50 , default='user')
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rank = models.ForeignKey(Rank, null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    # Opcionalmente puedes cambiar cómo se ve el usuario
    def __str__(self):
        return self.username
