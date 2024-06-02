# Fecha de Creación: 02/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 23/04/2024

from django.contrib import admin
from . models import User, UserAudit

#Registrar los modelos aquí
admin.site.register(User)
admin.site.register(UserAudit)




