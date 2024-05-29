# Generated by Django 5.0.2 on 2024-05-29 01:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiaprima', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='desinfeccion',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='desinfeccion',
            name='des_nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.desinfectantegenerico'),
        ),
        migrations.AddField(
            model_name='desinfeccion',
            name='mp_lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.materiaprima'),
        ),
        migrations.AddField(
            model_name='caracteristicasorganolepticas',
            name='mp_lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.materiaprima'),
        ),
        migrations.AddField(
            model_name='materiaprimaaudit',
            name='changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materiaprima.materiaprima'),
        ),
        migrations.AddField(
            model_name='materiaprimaaudit',
            name='materiaprima',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='materiaprima.materiaprima'),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='mp_nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaprima.materiaprimagenerica'),
        ),
    ]
