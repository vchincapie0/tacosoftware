from django.apps import AppConfig


class InsumosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.insumos'

    def ready(self):
        import applications.insumos.signals  # Importa tus señales aquí

