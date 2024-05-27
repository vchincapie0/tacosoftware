from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Facturas, IVA, FacturasAudit
import threading

@receiver(pre_save, sender=Facturas)
def calcular_total_factura(sender, instance, **kwargs):
    # Obtener el valor de IVA asociado a la factura
    iva_valor = instance.fac_iva.valor if instance.fac_iva else 0.0
    
    # Calcular el total como subtotal más IVA
    subtotal = instance.fac_subtotal
    total = subtotal+((subtotal * iva_valor)/100)  # Calcular el total con IVA
    # Asignar el total calculado a fac_total
    instance.fac_total = total

# Obtener el modelo de usuario personalizado
User = get_user_model()

@receiver(post_save, sender=Facturas)
def log_facturas_change(sender, instance, created, **kwargs):
    current_user = getattr(threading, 'current_user', None)

    if current_user:
        changed_by = current_user

    if instance.deleted:
        action = 'D'  # Marcar como eliminado
        details = f"{instance.num_factura} ha sido borrado."
    elif created:
        action = 'C'  # Creación de Pedidos
        details = f"{instance.num_factura} ha sido creado."
    else:
        action = 'U'  # Actualización de Pedidos
        details = f"La información de {instance.num_factura} ha sido actualizado."

    # Obtener el pedido asociado a la factura
    pedido_instance = instance.fac_numeroPedido

    # Obtener el proveedor asociado a la factura
    proveedor_instance=instance.fac_proveedor

    # Crear el registro de auditoría con el usuario que realizó la acción
    FacturasAudit.objects.create( 
        changed_by=changed_by,
        factura=instance, 
        pedido=pedido_instance, 
        proveedor=proveedor_instance, 
        action=action, 
        details=details)
