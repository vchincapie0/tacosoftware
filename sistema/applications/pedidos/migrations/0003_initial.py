# Generated by Django 5.0.2 on 2024-05-29 03:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='pedi_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pedidosaudit',
            name='changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pedidosaudit',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_logs', to='pedidos.pedidos'),
        ),
    ]
