# Fecha de Creación: 04/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 11/05/2024

from django.db import models
from django.utils import timezone
from applications.users.models import User

class Proveedores(models.Model):
    '''Clase para la creación de la tabla proveedores en la base de datos'''
    prov_id=models.AutoField('id',primary_key=True)
    nit = models.IntegerField('NIT',unique=True)
    prov_nombre=models.CharField('Nombre',max_length=40)
    prov_telefono=models.CharField('Telefono',max_length=10)
    deleted = models.BooleanField(default=False)  # Campo para el borrado lógico
    created=models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f"{self.prov_nombre}"
    
    def delete(self, using=None, keep_parents=False):
        '''Función para realizar el borrado lógico del proveedor'''
        self.deleted = True  # Marca el proveedor como inactivo en lugar de eliminarlo
        self.save(using=using)

class ProveedoresAudit(models.Model):
    '''Modelo para auditar cambios en los proveedores'''

    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado')
    ]

    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedores,on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_action_display()} - {self.changed_by} ({self.changed_at})'
