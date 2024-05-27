from django.apps import AppConfig


class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.pedidos'

    def ready(self):
        import applications.pedidos.signals