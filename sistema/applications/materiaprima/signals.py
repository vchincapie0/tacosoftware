from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CaracteristicasOrganolepticas, Desinfeccion, MateriaPrimaAudit, MateriaPrima
import threading

@receiver(pre_save, sender=CaracteristicasOrganolepticas)
def actualizar_estado(sender, instance, **kwargs):
    # Verificar si todas las características son iguales a cero
    if instance.olor == instance.textura == instance.limpieza == instance.empaque == instance.color == True:
        # Establecer el estado como 'Aprobado'
        instance.estado = '0'  # Suponiendo que '0' corresponde a 'Aprobado' según tus opciones
    else:
        instance.estado = '1'

# Obtener el modelo de producto personalizado
User = get_user_model()

@receiver(post_save, sender=MateriaPrima)
def log_user_change(sender, instance, created, **kwargs):
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    if created:
        action = 'C'  # Creación de producto
        details = f"{instance.mp_nombre} ha sido creado."
    else:
        action = 'U'  # Actualización de producto
        details = f"La información de {instance.mp_nombre} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    MateriaPrimaAudit.objects.create(materiaprima=instance, action=action, details=details, changed_by=changed_by)

@receiver(post_save, sender=MateriaPrima)
def actualizar_cantidad_total_insumo(sender, instance, **kwargs):
    insumo = instance.mp_nombre
    insumo.actualizar_cantidad_total()
    insumo.save()  # Guarda la materia prima después de actualizar la cantidad total