#Fecha de Creación: 02/02/2024
#Autor: Vivian Carolina Hincapie Escobar
#Última modficación: 17/05/2024

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.

class User(AbstractUser):
    '''Modelo de Usuario personalizado que hereda de AbstractUser'''

    # Campos personalizados para el usuario
    username = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_admin=models.BooleanField('Administrador',default=False)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Mantenemos is_active para funcionalidad estándar de Django
    deleted = models.BooleanField(default=False)  # Nuevo campo para el borrado lógico

    # Campos requeridos para el formulario de registro
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['name','last_name']

    objects = UserManager()# Utiliza un UserManager personalizado

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres+'-'+self.apellidos
    
    def delete(self, using=None, keep_parents=False):
        # Sobrescribe el método delete para realizar un borrado lógico
        self.is_active=False
        self.deleted = True
        self.save(using=using)

class UserAudit(models.Model):
    '''Modelo para auditar acciones de usuario'''

    # Elecciones para los tipos de acciones
    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado'),
        ('L', 'Inicio de Sesión'),
        ('O', 'Cerrado de Sesión')
    ]

    # Campos del modelo
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f'{self.get_action_display()} - {self.user.username} ({self.changed_at})'


