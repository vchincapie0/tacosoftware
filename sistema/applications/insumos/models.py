from django.db import models

# Create your models here.

class InsumosGenerico(models.Model):
    '''Tabla generica para insumos'''
    it_nombre=models.CharField('Nombre',max_length=50)
    cantidad_total = models.IntegerField('Cantidad Total', default=0)  # Nuevo campo para almacenar la cantidad total
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.it_nombre}"
    
    def actualizar_cantidad_total(self):
        total = sum([insumo.it_cantidad for insumo in self.insumos_set.all()])
        self.cantidad_total = total
        self.save()
    
class Insumos(models.Model):
    
    class Estado(models.TextChoices):
        DISPONIBLE = '0', 'Disponible'
        NO_DISPONIBLE = '1', 'No Disponible'

    it_codigo = models.AutoField(primary_key=True)
    it_nombre = models.ForeignKey(InsumosGenerico, on_delete=models.CASCADE)
    it_cantidad = models.IntegerField('Cantidad')
    it_fechaEntrega = models.DateField('Fecha Entrega')
    it_estado = models.CharField('Estado', max_length=1, choices=Estado.choices)
    deleted = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.it_codigo}-{self.it_nombre}-{self.it_fechaEntrega}"

    def save(self, *args, **kwargs):
        # Condiciona el estado basándote en el campo it_cantidad
        if self.it_cantidad == 0:
            self.it_estado = self.Estado.NO_DISPONIBLE
        else:
            self.it_estado = self.Estado.DISPONIBLE

        super().save(*args, **kwargs)

class InsumosAudit(models.Model):
    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado')
    ]

    insumos = models.ForeignKey(Insumos, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(Insumos, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_action_display()} - {self.insumos.it_nombre} ({self.changed_at})'
