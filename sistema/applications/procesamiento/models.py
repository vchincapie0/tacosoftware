from django.db import models
from applications.productoterminado.models import ProductoTerminadoGenerico

# Create your models here.
class Picado(models.Model):

    ESTADO_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),

    )

    cod_procesamiento=models.AutoField(primary_key=True)
    pica_producto=models.ManyToManyField(ProductoTerminadoGenerico, blank=True)
    pica_cantidad = models.IntegerField('Cantidad',default=0)
    pica_pesoMPposproceso=models.FloatField('Peso',default=0)
    pica_merma=models.FloatField('Peso Merma',default=0)
    pica_check=models.CharField('estado',max_length=1, choices=ESTADO_CHOICES)
    
    def __str__(self):
        return f"{self.pica_producto}-{self.pica_cantidad}{self.pica_pesoMPposproceso}-{self.pica_merma}-{self.pica_check}"


class Equipos(models.Model):

    CHECK_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),

    )

    id_equipo=models.AutoField(primary_key=True)
    equi_encargadoCocina=models.CharField('Nombre', max_length=50,default="NULL")
    equi_encargadoEntrega=models.CharField('Nombre', max_length=50,default="NULL")
    equi_calidad=models.CharField('estado',max_length=1, choices=CHECK_CHOICES,default="0")
    equi_nombre=models.CharField('Nombre', max_length=50,default="NULL")
    equi_check=models.CharField('estado',max_length=1, choices=CHECK_CHOICES, default="0")
    deleted = models.BooleanField(default=False) #Campo que corresponde al borrado logico

    
    def __str__(self):
        return f"{self.id_equipo}-{self.equi_encargadoCocina}-{self.equi_encargadoEntrega}-{self.equi_nombre}"
    
    def delete(self, using=None, keep_parents=False):
        '''Funcion para borrado lógico'''
        self.deleted = True  # Marcar como inactivo en lugar de eliminar
        self.save(using=using)

class Coccion(models.Model):

    CHECK_CHOICES=(
        ('0','Aceptado'),
        ('1','Rechazado'),

    )

    id_coccion=models.AutoField(primary_key=True)
    cocc_producto=models.ManyToManyField(ProductoTerminadoGenerico, blank=True)
    cocc_cantidad = models.IntegerField('Cantidad',default=0)
    cocc_pesoMPposproceso=models.FloatField('Peso',default=0)
    cocc_merma=models.FloatField('Peso Merma',default=0)
    cocc_tiempoCoccion=models.TimeField(default=100)
    cocc_temperaturafinal=models.FloatField('temperatura final')
    cocc_check=models.CharField('estado',max_length=1, choices=CHECK_CHOICES,default="0")

    
    def __str__(self):
        return f"{self.id_coccion}-{self.cocc_cantidad}-{self.cocc_pesoMPposproceso}-{self.cocc_merma}-{self.cocc_tiempoCoccion}-{self.cocc_temperaturafinal}-{self.cocc_check}"


