from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import InsumosAudit, Insumos, InsumosGenerico
import threading

# Obtener el modelo de implementos personalizados
User = get_user_model()

@receiver(post_save, sender=InsumosAudit)
def log_user_change(sender, instance, created, **kwargs):
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.it_nombre} ha sido borrado."
    elif created:
        action = 'C'  # Creación de producto
        details = f"{instance.it_nombre} ha sido creado."
    else:
        action = 'U'  # Actualización de producto
        details = f"La información de {instance.it_nombre} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    InsumosAudit.objects.create(insumos=instance, action=action, details=details, changed_by=changed_by)


@receiver(post_save, sender=Insumos)
@receiver(post_delete, sender=Insumos)
def actualizar_cantidad_total_insumo(sender, instance, **kwargs):
    print('Dentro de señal cantidad')
    insumo = instance.it_nombre
    insumo.actualizar_cantidad_total()
    insumo.save()  # Guarda el insumo después de actualizar la cantidad total