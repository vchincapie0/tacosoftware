from django.apps import AppConfig


class FacturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.facturas'

    def ready(self):
        import applications.facturas.signals  # Importa tus señales aquí
