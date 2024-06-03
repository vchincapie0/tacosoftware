# Fecha de Creación: 02/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 29/04/2024

from django.apps import AppConfig


class ProveedoresConfig(AppConfig):
    """
    Configuración de la aplicación 'proveedores'.
    """

    # Especifica el campo predeterminado para las claves primarias automáticas en los modelos
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación, utilizado en la configuración del proyecto
    name = 'applications.proveedores'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Importa los módulos de señales para registrar los manejadores de señales.
        """
        import applications.proveedores.signals
