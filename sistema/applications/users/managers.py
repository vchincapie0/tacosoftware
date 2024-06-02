# Fecha de Creación: 02/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 16/02/2024

from django.db import models
from django.contrib.auth.models import BaseUserManager

# Clase UserManager: un administrador de usuarios personalizado que extiende BaseUserManager y models.Manager
class UserManager(BaseUserManager, models.Manager):

    # Método para crear un usuario básico
    def _create_user(self, name, last_name, username, password, is_staff, is_superuser, **extra_fields):
        # Crea una nueva instancia de usuario con los campos proporcionados
        user = self.model(
            name=name,
            last_name=last_name,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        # Establece la contraseña del usuario y guarda el usuario en la base de datos
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    # Método para crear un usuario normal
    def create_user(self, name, last_name, username, password=None, **extra_fields):
        # Llama a _create_user con is_staff y is_superuser establecidos en False
        return self._create_user(name, last_name, username, password, False, False, **extra_fields)

    # Método para crear un superusuario
    def create_superuser(self, name, last_name, username, password=None, **extra_fields):
        # Llama a _create_user con is_staff y is_superuser establecidos en True
        return self._create_user(name, last_name, username, password, True, True, **extra_fields)
