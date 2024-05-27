from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, name, last_name,username, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            name=name,
            last_name=last_name,
            username = username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, name, last_name,username,password=None,**extrafields):
        return self._create_user(name,last_name,username, password,False,False, **extrafields)

    def create_superuser(self, name,last_name,username, password=None, **extra_fields):
        return self._create_user(name,last_name,username,password, True, True,**extra_fields)



