from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    email = models.EmailField(unique=True)
    matricula = models.CharField('matricula', max_length=20, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'matricula']
