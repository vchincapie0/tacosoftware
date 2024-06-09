# Fecha de Creación: 29/04/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Proveedores, ProveedoresAudit
import threading

# Obtener el modelo de usuario personalizado
User = get_user_model()

@receiver(post_save, sender=Proveedores)
def log_pedidos_change(sender, instance, created, **kwargs):
    '''Función para registrar cambios en el modelo Proveedores'''

    # Obtener el usuario actual del hilo (si está disponible)
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    # Determinar la acción realizada y los detalles del cambio
    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.prov_nombre} ha sido borrado."
    elif created:
        action = 'C'  # Creación de Pedidos
        details = f"{instance.prov_nombre} ha sido creado."
    else:
        action = 'U'  # Actualización de Pedidos
        details = f"La información de {instance.prov_nombre} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    ProveedoresAudit.objects.create( changed_by=changed_by, proveedor=instance, action=action, details=details)
