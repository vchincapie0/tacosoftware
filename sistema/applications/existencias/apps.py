# Fecha de Creación: 14/04/2024
# Autor: Vivian Carolina Hincapie Escobar 
# Última modificación: 21/05/2024

from django.apps import AppConfig

class ExistenciasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.existencias'

    def ready(self):
        import applications.existencias.signals  # Importa tus señales aquí

