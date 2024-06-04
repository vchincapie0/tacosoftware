# Fecha de Creación: 20/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.contrib import admin
from .models import Pedidos, PedidosAudit

admin.site.register(Pedidos)
admin.site.register(PedidosAudit)
