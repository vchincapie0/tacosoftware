from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CaracteristicasOrganolepticasPT,ProductoTerminadoAudit
import threading

@receiver(pre_save, sender=CaracteristicasOrganolepticasPT)
def actualizar_estado(sender, instance, **kwargs):
    # Verificar si todas las características son iguales a cero
    if instance.olor == instance.textura == instance.sabor == instance.color == True:
        # Establecer el estado como 'Aprobado'
        instance.estado = '0'  # Suponiendo que '0' corresponde a 'Aprobado' según tus opciones
    else:
        instance.estado = '1'

# Obtener el modelo de producto personalizado
User = get_user_model()

@receiver(post_save, sender=ProductoTerminadoAudit)
def log_user_change(sender, instance, created, **kwargs):
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.pt_nombre} ha sido borrado."
    elif created:
        action = 'C'  # Creación de producto
        details = f"{instance.pt_nombre} ha sido creado."
    else:
        action = 'U'  # Actualización de producto
        details = f"La información de {instance.pt_nombre} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    ProductoTerminadoAudit.objects.create(productoterminado=instance, action=action, details=details, changed_by=changed_by)
