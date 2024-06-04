# Fecha de Creación: 20/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.apps import AppConfig

class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.pedidos'

    def ready(self):
        import applications.pedidos.signals