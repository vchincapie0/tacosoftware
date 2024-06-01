import random
import string
from django.db import models
from django.utils import timezone
from applications.materiaprima.models import MateriaPrimaGenerica

# Creacion model Producto terminado.

class ProductoTerminadoGenerico(models.Model):
    '''Tabla generica que mostrara los distintos productos terminados que se producen'''
    TIPO_CHOICES=(
        ('0','Cocción'),
        ('1','Picado'),
    )
    pt_nombre=models.CharField('Nombre Producto Terminado', max_length=50)
    materiaPrimaUsada=models.ManyToManyField(MateriaPrimaGenerica)
    pt_tipo=models.CharField('Tipo',max_length=1,choices=TIPO_CHOICES,default=0)
    

    def __str__(self):
        return f"{self.pt_nombre}"

class ProductoTerminado(models.Model):
    '''Clase para la creacion de tabla de producto terminado'''
    pt_lote= models.CharField(max_length=8, unique=True, editable=False)
    pt_cantidad=models.IntegerField()
    pt_nombre=models.ForeignKey(ProductoTerminadoGenerico,on_delete=models.CASCADE)
    pt_fechapreparacion=models.DateField('Fecha Preparacion',default=timezone.now)
    pt_fechavencimiento=models.DateField('Fecha Vencimiento')

    def save(self, *args, **kwargs):
        if not self.pt_lote:
            self.pt_lote = 'PT' + ''.join(random.choices(string.digits, k=4))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pt_lote}-{self.pt_nombre}"

class ExistenciaPT(models.Model):

    pt_lote=models.ForeignKey(ProductoTerminado,on_delete=models.CASCADE)
    exisPT_CantidadIngresada = models.IntegerField('Cantidad Ingresada')
    exisPT_CantidadEgresada = models.IntegerField('Cantidad Egresada')


    def __str__(self):
        return f"{self.pt_lote}-{self.exisPT_CantidadIngresada}-{self.exisPT_CantidadEgresada}"
  
class CaracteristicasOrganolepticasPT(models.Model):

    ESTADO_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),
    )

    producto=models.ForeignKey(ProductoTerminado,on_delete=models.CASCADE)
    observaciones = models.CharField('Observaciones', max_length=50)
    olor = models.BooleanField('Olor',default=False)
    sabor = models.BooleanField('Sabor',default=False)
    textura = models.BooleanField('Textura',default=False)
    color = models.BooleanField('Color',default=False)
    estado=models.CharField('Estado',max_length=1,choices=ESTADO_CHOICES, default=0)
    
    def __str__(self):
        return str(self.pt_lote)+'-'+self.estado

class EmpaqueProductoTerminado(models.Model):

    pt_lote=models.ForeignKey(ProductoTerminado,on_delete=models.CASCADE)
    emp_pesoKg = models.FloatField('Peso Empaque')
    emp_cantidadBolsas = models.IntegerField('Cantidad Bolsas')


    def __str__(self):
        return f"{self.pt_lote}-{self.emp_pesoKg}-{self.emp_cantidadBolsas}"

class Vacio(models.Model):

    pt_lote=models.ForeignKey(ProductoTerminado,on_delete=models.CASCADE)
    cantidad_bolsas_rechazadas = models.IntegerField('Cantidad Bolsas Rechazadas')
    cantidad_bolsas_liberadas = models.IntegerField('Cantidad Bolsas Liberadas')


    def __str__(self):
        return f"{self.pt_lote}-{self.cantidad_bolsas_rechazadas}"

class ProductoTerminadoAudit(models.Model):
    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado')
    ]

    productoterminado = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(ProductoTerminado, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_action_display()} - {self.productoterminado.pt_nombre} ({self.changed_at})'
