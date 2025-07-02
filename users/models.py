from django.contrib.auth.models import AbstractUser
from django.db import models
from facilities.models import Instalacion

class CustomUser(AbstractUser):
    CAPTADOR = 'default'
    COORDINADOR = 'coordinador'
      
    ROLE_CHOICES = (
        (CAPTADOR, 'Captador'),
        (COORDINADOR, 'Coordinador'),
    )

    instalaciones = models.ManyToManyField(Instalacion, blank=True)
    role = models.CharField("Rol", max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
