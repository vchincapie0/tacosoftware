from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Pedidos, PedidosAudit
import threading



# Obtener el modelo de usuario personalizado
User = get_user_model()

@receiver(post_save, sender=Pedidos)
def log_pedidos_change(sender, instance, created, **kwargs):
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

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
