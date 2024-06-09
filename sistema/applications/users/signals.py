#Fecha de Creación: 22/04/2024
#Autor: Vivian Carolina Hincapie Escobar
#Última modficación: 17/05/2024

from django.contrib.auth.signals import user_logged_in, user_logged_out
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import User, UserAudit

# Obtener el modelo de usuario personalizado
User = get_user_model()

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    '''Señal para validar que el usuario inicie sesion para auditorias'''
    current_user = user  # El usuario que se ha autenticado
    details = f"{current_user.name} {current_user.last_name} ha iniciado sesión."
    UserAudit.objects.create(user=current_user, action='L', details=details, changed_by=current_user)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    '''Señal para validar que el usuario cierre sesion para auditorias'''
    current_user = user  # El usuario que se ha desconectado
    details = f"{current_user.name} {current_user.last_name} ha cerrado sesión."
    UserAudit.objects.create(user=current_user, action='O', details=details, changed_by=current_user)

@receiver(post_save, sender=User)
def log_user_change(sender, instance, created, **kwargs):
    '''Señal para validar si el usuario se crea, modifica o se borra para auditorias'''
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.name} {instance.last_name} ha sido borrado."
    elif created:
        action = 'C'  # Creación de usuario
        details = f"{instance.name} {instance.last_name} ha sido creado."
    else:
        action = 'U'  # Actualización de usuario
        details = f"La información de {instance.name} {instance.last_name} ha sido actualizado."

    # Crear el registro de auditoría con el usuario que realizó la acción
    UserAudit.objects.create(user=instance, action=action, details=details, changed_by=changed_by)
