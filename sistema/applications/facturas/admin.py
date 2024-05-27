from django.contrib import admin
from .models import Facturas, IVA, FacturasAudit

# Register your models here.

class FacturasAdmin(admin.ModelAdmin):

    #Muestra los datos en forma mas estetica en admin
    list_display=(
        'num_factura',
        'fac_proveedor',
        'fac_numeroPedido',
        'fac_total',    
    )

admin.site.register(Facturas, FacturasAdmin)
admin.site.register(IVA)
admin.site.register(FacturasAudit)
