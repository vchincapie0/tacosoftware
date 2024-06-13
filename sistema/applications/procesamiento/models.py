from django.db import models
from applications.productoterminado.models import ProductoTerminado
from applications.materiaprima.models import MateriaPrimaGenerica
from applications.users.models import User

class Picado(models.Model):

    ESTADO_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),

    )

    pica_id=models.AutoField(primary_key=True)
    pica_producto=models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    pica_cantidad_total = models.IntegerField('Cantidad',default=0)
    pica_pesoPostProcesamiento=models.FloatField('Peso',default=0)
    pica_merma=models.FloatField('Peso Merma',default=0)
    pica_check=models.CharField('estado',max_length=1, choices=ESTADO_CHOICES)
    
    def __str__(self):
        return f"{self.pica_producto}-{self.pica_cantidad_total}{self.pica_pesoPostProcesamiento}-{self.pica_merma}-{self.pica_check}"

class PicadoMateriaPrima(models.Model):
    picado = models.ForeignKey(Picado, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrimaGenerica, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.picado} - {self.materia_prima} ({self.cantidad}g)"

class Coccion(models.Model):

    CHECK_CHOICES=(
        ('0','Aceptado'),
        ('1','Rechazado'),

    )

    cocc_id=models.AutoField(primary_key=True)
    cocc_producto=models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    cocc_cantidad_total = models.IntegerField('Cantidad',default=0)
    cocc_pesoPostProcesamiento=models.FloatField('Peso',default=0)
    cocc_merma=models.FloatField('Merma',default=0)
    cocc_tiempoCoccion=models.IntegerField('Tiempo de Coccion')
    cocc_temperaturafinal=models.FloatField('Temperatura final')
    cocc_check=models.CharField('estado',max_length=1, choices=CHECK_CHOICES,default="0")

    
    def __str__(self):
        return f"{self.cocc_producto}-{self.cocc_cantidad_total}-{self.cocc_pesoPostProcesamiento}-{self.cocc_merma}-{self.cocc_tiempoCoccion}-{self.cocc_temperaturafinal}-{self.cocc_check}"

class CoccionMateriaPrima(models.Model):
    coccion = models.ForeignKey(Coccion, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrimaGenerica, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.coccion} - {self.materia_prima} ({self.cantidad}g)"
    
class Equipos(models.Model):

    CHECK_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),

    )

    id_equipo=models.AutoField(primary_key=True)
    equi_encargadoCocina=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True, related_name='equipos_cocina')
    equi_encargadoEntrega=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True, related_name='equipos_entrega')
    equi_nombre=models.CharField('Nombre', max_length=50, default="NULL")
    equi_check=models.CharField('estado',max_length=1, choices=CHECK_CHOICES, default="0")
    deleted = models.BooleanField(default=False) #Campo que corresponde al borrado logico

    def __str__(self):
        return f"{self.id_equipo}-{self.equi_encargadoCocina}-{self.equi_encargadoEntrega}-{self.equi_nombre}"
    
    def delete(self, using=None, keep_parents=False):
        '''Funcion para borrado lógico'''
        self.deleted = True  # Marcar como inactivo en lugar de eliminar
        self.save(using=using)
