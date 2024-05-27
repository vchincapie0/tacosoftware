from django.apps import AppConfig


class ProductofinalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.productoterminado'

    def ready(self):
        import applications.productoterminado.signals  # Importa tus señales aquí