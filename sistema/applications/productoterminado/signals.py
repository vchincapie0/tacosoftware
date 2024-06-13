from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CaracteristicasOrganolepticasPT,ProductoTerminadoAudit, ProductoTerminado
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

@receiver(post_save, sender=ProductoTerminado)
def log_user_change(sender, instance, created, **kwargs):
    if created:
        action = 'C'  # Creación de producto
        details = f"{instance.pt_lote} ha sido creado."
    else:
        action = 'U'  # Actualización de producto
        details = f"La información de {instance.pt_lote} ha sido actualizado."

    # Obtener el usuario que realizó la acción
    current_user = getattr(threading, 'current_user', None)
    
    if current_user:
        changed_by = User.objects.get(username=current_user.username)
    else:
        changed_by = None

    # Crear el registro de auditoría con el usuario que realizó la acción
    ProductoTerminadoAudit.objects.create(productoterminado=instance, action=action, details=details, changed_by=changed_by)
