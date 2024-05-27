from django.apps import AppConfig


class MateriaprimaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.materiaprima'

    def ready(self):
        import applications.materiaprima.signals  # Importa tus señales aquí
