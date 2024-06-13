# Generated by Django 5.0.2 on 2024-06-12 20:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procesamiento', '0003_alter_coccion_cocc_producto_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipos',
            name='equi_calidad',
        ),
        migrations.AlterField(
            model_name='equipos',
            name='equi_encargadoCocina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipos_cocina', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipos',
            name='equi_encargadoEntrega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipos_entrega', to=settings.AUTH_USER_MODEL),
        ),
    ]
