# Fecha de Creación: 27/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.contrib import admin
from .models import Facturas, IVA, FacturasAudit

class FacturasAdmin(admin.ModelAdmin):
    #Muestra los datos en forma mas estetica en admin
    list_display=(
        'num_factura',
        'fac_numeroPedido',
        'fac_total',    
    )

# Registro de los modelos en la interfaz de administración de Django
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(IVA)
admin.site.register(FacturasAudit)
