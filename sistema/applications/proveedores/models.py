from django.db import models
from django.utils import timezone
from applications.users.models import User

# Create your models here.

class Proveedores(models.Model):
    '''Clase para la creacion de tabla proveedores en bd'''
    prov_id=models.AutoField('id',primary_key=True)
    nit = models.IntegerField('NIT',unique=True)
    prov_nombre=models.CharField('Nombre',max_length=40)
    prov_telefono=models.CharField('Telefono',max_length=10)
    deleted = models.BooleanField(default=False)  # Campo para el borrado lógico
    created=models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f"{self.prov_nombre}"
    
    def delete(self, using=None, keep_parents=False):
        '''Funcion para borrado lógico'''
        self.deleted = True  # Marcar como inactivo en lugar de eliminar
        self.save(using=using)

class ProveedoresAudit(models.Model):
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
