# Fecha de Creación: 27/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 11/04/2024

from django.apps import AppConfig

class FacturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.facturas'

    def ready(self):
        import applications.facturas.signals  # Importa tus señales aquí
