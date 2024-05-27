from django.contrib import admin
from .models import Pedidos, PedidosAudit

# Register your models here.

admin.site.register(Pedidos)
admin.site.register(PedidosAudit)
