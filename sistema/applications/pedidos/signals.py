# Fecha de Creación: 18/03/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Pedidos, PedidosAudit
import threading

# Obtener el modelo de usuario personalizado
User = get_user_model()

@receiver(post_save, sender=Pedidos)
def log_pedidos_change(sender, instance, created, **kwargs):
    '''Definición de la función que maneja la señal después de guardar un objeto Pedidos'''
    current_user = getattr(threading, 'current_user', None)

    # Obtener el usuario actual que realizó la acción
    if current_user:
        changed_by = current_user

    # Determinar la acción realizada y los detalles para el registro de auditoría
    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.ref_pedido} ha sido borrado."
    elif created:
        action = 'C'  # Creación de Pedidos
        details = f"{instance.ref_pedido} ha sido creado."
    else:
        action = 'U'  # Actualización de Pedidos
        details = f"La información de {instance.ref_pedido} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    PedidosAudit.objects.create( changed_by=changed_by, pedido=instance, action=action, details=details)
