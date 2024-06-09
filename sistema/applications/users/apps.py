# Fecha de Creación: 02/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 23/04/2024

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.users'

    def ready(self):
        import applications.users.signals