from django.contrib import admin
from . models import User, UserAudit

# Register your models here.

admin.site.register(User)
admin.site.register(UserAudit)




