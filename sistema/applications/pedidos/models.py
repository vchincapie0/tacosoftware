# Fecha de Creación: 20/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.db import models
from applications.users.models import User
from applications.materiaprima.models import MateriaPrima
from applications.insumos.models import Insumos
from applications.proveedores.models import Proveedores
from django.utils import timezone

class Pedidos(models.Model):
    '''Definición del modelo para los pedidos'''

    # Opciones para el estado del pedido
    ESTADO_CHOICES=(
        ('0','Completo'),
        ('1','Incompleto'),
        ('2','Rechazado'),
    )

    id=models.AutoField('id',primary_key=True)
    ref_pedido=models.IntegerField('Referencia',unique=True)
    pedi_user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank= True)
    pedi_fecha=models.DateField('fecha',default=timezone.now)
    pedi_estado=models.CharField('estado',max_length=1, choices=ESTADO_CHOICES)
    pedi_comprobatePago=models.CharField('Comprobante Pago',max_length=45)
    pedi_proveedor=models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    pedi_materiaprima=models.ManyToManyField(MateriaPrima, blank=True)
    pedi_insumos=models.ManyToManyField(Insumos, blank=True)
    deleted = models.BooleanField(default=False)  # Campo para el borrado lógico

    def __str__(self):
        estado = dict(self.ESTADO_CHOICES)[self.pedi_estado] if self.pedi_estado else 'Estado Desconocido'
        return f"N° Pedido: {self.ref_pedido} - Estado: {estado}"

    def delete(self, using=None, keep_parents=False):
        '''Función para borrado lógico'''
        self.deleted = True # Marcar como inactivo en lugar de eliminar
        self.save(using=using)

class PedidosAudit(models.Model):
    '''Definición del modelo para el registro de auditoría de pedidos'''

    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado')
    ]

    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedidos,on_delete=models.CASCADE, related_name='pedidos_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_action_display()} - {self.changed_by} ({self.changed_at})'
