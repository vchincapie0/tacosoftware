from django.db import models
from applications.users.models import User
from django.utils import timezone

# Create your models here.
class MateriaPrimaGenerica(models.Model):
    '''Tabla de materia prima generica'''
    TIPO_CHOICES=(
        ('0','Proteina'),
        ('1','Lácteo'),
        ('2','Verduras'),
        ('3','Frutas'),
        ('4','Otros'),

    )

    mp_nombre=models.CharField('Nombre',max_length=50)
    mp_tipo=models.CharField('Tipo',max_length=1,choices=TIPO_CHOICES,default=0)
    cantidad_total = models.IntegerField('Cantidad Total', default=0)  # Nuevo campo para almacenar la cantidad total
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mp_nombre}"
    
    def actualizar_cantidad_total(self):
        # Verificar si existen características organolépticas aprobadas y desinfección asociada
        total = sum([materia.mp_cantidad for materia in self.materiaprima_set.all()])
        self.cantidad_total = total
        self.save()
  
class MateriaPrima(models.Model):
    ''''Tabla de materia prima con caracteristicas'''
    

    mp_lote = models.IntegerField('Lote', primary_key=True)
    mp_nombre = models.ForeignKey(MateriaPrimaGenerica, on_delete=models.CASCADE)
    mp_cantidad=models.IntegerField(default=100)
    mp_fechallegada=models.DateField('Fecha Ingreso',default=timezone.now)
    mp_fechavencimiento = models.DateField('Fecha Vencimiento',default=timezone.now)

    def __str__(self):
        return str(self.mp_lote)+'-'+str(self.mp_nombre)

class CaracteristicasOrganolepticas(models.Model):
    '''Tabla para caracteristicas organolepticas de materiaprima'''
    ESTADO_CHOICES=(
        ('0','Aprobado'),
        ('1','No Aprobado'),
    )

    mp_lote=models.ForeignKey(MateriaPrima,on_delete=models.CASCADE)
    olor = models.BooleanField('Olor',default=False)
    textura = models.BooleanField('Textura',default=False)
    limpieza = models.BooleanField('Limpieza',default=False)
    empaque = models.BooleanField('Empaque',default=False)
    color = models.BooleanField('Color',default=False)
    estado=models.CharField('Estado',max_length=1,choices=ESTADO_CHOICES)
    
    def __str__(self):
        return str(self.mp_lote)+'-'+self.estado
    
class DesinfectanteGenerico(models.Model):
    '''Tabla generica para desinfectantes'''
    des_nombre=models.CharField('Nombre',max_length=50)
    
    def __str__(self):
        return f"{self.des_nombre}"
    
class Desinfeccion(models.Model):
    '''Tabla de desinfección de materia prima'''
    mp_lote=models.ForeignKey(MateriaPrima,on_delete=models.CASCADE)
    des_nombre=models.ForeignKey(DesinfectanteGenerico, on_delete=models.CASCADE)
    concentracion = models.IntegerField('Concentración')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tiempo_inicio=models.TimeField('Tiempo de Inicio')
    tiempo_fin=models.TimeField('Fin Desinfección')
    obsevacion=models.CharField('Observaciones',max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.mp_lote)+'-'+str(self.des_nombre)
    
class MateriaPrimaAudit(models.Model):
    ACTION_CHOICES = [
        ('C', 'Creado'),
        ('U', 'Actualizado'),
        ('D', 'Borrado')
    ]

    materiaprima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(MateriaPrima, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_action_display()} - {self.materiaprima.mp_nombre} ({self.changed_at})'

    


    
