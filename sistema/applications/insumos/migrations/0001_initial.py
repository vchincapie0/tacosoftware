# Generated by Django 5.0.2 on 2024-05-29 03:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insumos',
            fields=[
                ('it_codigo', models.AutoField(primary_key=True, serialize=False)),
                ('it_cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('it_fechaEntrega', models.DateField(verbose_name='Fecha Entrega')),
                ('it_estado', models.CharField(choices=[('0', 'Disponible'), ('1', 'No Disponible')], max_length=1, verbose_name='Estado')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InsumosGenerico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('it_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('cantidad_total', models.IntegerField(default=0, verbose_name='Cantidad Total')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InsumosAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('C', 'Creado'), ('U', 'Actualizado'), ('D', 'Borrado')], max_length=1)),
                ('details', models.TextField(blank=True, null=True)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='insumos.insumos')),
                ('insumos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='insumos.insumos')),
            ],
        ),
        migrations.AddField(
            model_name='insumos',
            name='it_nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumos.insumosgenerico'),
        ),
    ]
