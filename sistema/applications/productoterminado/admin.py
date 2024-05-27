from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProductoTerminadoGenerico)
admin.site.register(ProductoTerminado)
admin.site.register(CaracteristicasOrganolepticasPT)
admin.site.register(EmpaqueProductoTerminado)
admin.site.register(Vacio)

