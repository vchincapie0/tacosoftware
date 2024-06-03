# Fecha de Creación: 02/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.contrib import admin
from .models import Proveedores, ProveedoresAudit

# Registro de los modelos en el sitio de administración de Django.
# Esto permite gestionar los modelos Proveedores y ProveedoresAudit a través del panel de administración.

admin.site.register(Proveedores)
admin.site.register(ProveedoresAudit)
