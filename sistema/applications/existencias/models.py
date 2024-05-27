from django.db import models
from applications.materiaprima.models import MateriaPrima 

class ExistenciaMp(models.Model):
    '''Tabla de existencias de materia prima'''
    codigo=models.PositiveIntegerField('Código', primary_key=True)
    mp_lote=models.ForeignKey(MateriaPrima,on_delete=models.CASCADE)
    cantidadIngresada=models.PositiveIntegerField('Cantidad Ingresada')
    cantidadEgresada=models.PositiveIntegerField('Cantidad Egresada')
    def __str__(self):
        return f"{self.mp_lote} - {self.cantidadIngresada} - {self.cantidadEgresada}"