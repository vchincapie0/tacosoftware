# Generated by Django 5.0.2 on 2024-06-12 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0005_remove_facturas_fac_proveedor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facturas',
            options={'verbose_name': 'Factura', 'verbose_name_plural': 'Factura'},
        ),
        migrations.AlterModelOptions(
            name='facturasaudit',
            options={'verbose_name': 'Auditoria de Factura', 'verbose_name_plural': 'Auditorias de Facturas'},
        ),
        migrations.AlterModelOptions(
            name='iva',
            options={'verbose_name': 'IVA', 'verbose_name_plural': 'IVA'},
        ),
    ]
