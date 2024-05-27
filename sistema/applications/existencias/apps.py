from django.apps import AppConfig


class ExistenciasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.existencias'

    def ready(self):
        import applications.existencias.signals  # Importa tus señales aquí

