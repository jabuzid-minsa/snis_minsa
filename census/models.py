from django.db import models
from political_division.models import Poblado 

class Population(models.Model):
    contra_key = models.ForeignKey(Poblado, to_field="contra_key", null=True, on_delete=models.SET_NULL, verbose_name="Población")
    indigenous = models.IntegerField("Indígena", null=True, blank=True)
    non_indigenous = models.IntegerField("No indígena", null=True, blank=True)
    residences = models.IntegerField("Total de viviendas", null=True, blank=True)

    class Meta:
        verbose_name = 'Población'
        verbose_name_plural = 'Población'
    
    def __str__(self):
        return ''