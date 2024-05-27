from django import forms
from django.utils import timezone
from .models import MateriaPrima, Desinfeccion, CaracteristicasOrganolepticas,MateriaPrimaGenerica, DesinfectanteGenerico,MateriaPrimaAudit
from applications.users.models import User

class MateriaPrimaGenericaUpdateForm(forms.ModelForm):
    """Form definition for Materia Prima."""

    class Meta:
        """Meta definition for MateriaPrimaform."""

        model = MateriaPrimaGenerica
        fields = (
            'mp_nombre',
            'mp_tipo',
            )
        widgets={
            'mp_nombre':forms.TextInput(attrs={'class':'form-control'}),
            'mp_tipo':forms.Select(attrs={'class':'form-select'}),
        }

class MateriaPrimaGenericaForm(forms.ModelForm):
    """Form definition for Materia Prima."""

    class Meta:
        """Meta definition for MateriaPrimaform."""

        model = MateriaPrimaGenerica
        fields = (
            'mp_nombre',
            'mp_tipo',
            )
        widgets={
            'mp_nombre':forms.TextInput(attrs={'class':'form-control'}),
            'mp_tipo':forms.Select(attrs={'class':'form-select'}),
        }

class MateriaPrimaUpdateForm(forms.ModelForm):
    """Form definition for update Materia Prima."""

    class Meta:
        """Meta definition for update MateriaPrimaform."""

        model = MateriaPrima
        fields = (
            'mp_lote',
            'mp_nombre',
            'mp_cantidad',
            'mp_fechallegada',
            'mp_fechavencimiento',
            )
        
        widgets={
            'mp_lote':forms.NumberInput(attrs={'class':'form-control'}),
            'mp_nombre':forms.Select(attrs={'class':'form-select'}),
            'mp_cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'mp_fechallegada':forms.SelectDateWidget(),
            'mp_fechavencimiento':forms.SelectDateWidget(),
        }
    
    def clean_mp_cantidad(self):
        cantidad = self.cleaned_data['mp_cantidad']
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
        return cantidad
    
    def clean_mp_fechallegada(self):
        fecha_llegada = self.cleaned_data['mp_fechallegada']
        fecha_actual = timezone.now().date()
        tres_dias_atras = fecha_actual - timezone.timedelta(days=3)

        # Comprueba si la fecha de llegada está dentro del rango permitido
        if fecha_llegada > fecha_actual or fecha_llegada < tres_dias_atras:
            raise forms.ValidationError('La fecha de llegada debe ser el día actual o hasta 3 días antes.')
        
        return fecha_llegada
    
    def clean_mp_fechavencimiento(self):
        fecha_vencimiento = self.cleaned_data['mp_fechavencimiento']
        fecha_actual = timezone.now().date()

        # Comprueba si la fecha de vencimiento es anterior a la fecha actual
        if fecha_vencimiento < fecha_actual:
            raise forms.ValidationError('La fecha de vencimiento debe ser posterior a la fecha actual.')

        return fecha_vencimiento

class CaracteristicasMPForm(forms.ModelForm):

    class Meta:

        model = CaracteristicasOrganolepticas
        fields=(
            'mp_lote',
            'olor',
            'textura',
            'limpieza',
            'empaque',
            'color',
             
        )

        widgets={
                'olor':forms.CheckboxInput(),
                'textura':forms.CheckboxInput(),
                'limpieza':forms.CheckboxInput(),
                'empaque':forms.CheckboxInput(),
                'color':forms.CheckboxInput(),    
            }
        
class CaracteristicasMPUpdateForm(forms.ModelForm):

    class Meta:

        model = CaracteristicasOrganolepticas
        fields=(
            'mp_lote',
            'olor',
            'textura',
            'limpieza',
            'empaque',
            'color',
             
        )

        widgets={
                'mp_lote':forms.TextInput(attrs={'class':'form-control'}),
                'olor':forms.CheckboxInput(),
                'textura':forms.CheckboxInput(),
                'limpieza':forms.CheckboxInput(),
                'empaque':forms.CheckboxInput(),
                'color':forms.CheckboxInput(),    
            }
                       
class DesinfeccionMPForm(forms.ModelForm):


    class Meta:

        model = Desinfeccion
        fields=(
            'mp_lote',
            'des_nombre',
            'concentracion',
            'tiempo_inicio',
            'tiempo_fin',
            'obsevacion', 
             
        )

        widgets={
            'mp_lote':forms.Select(attrs={'class':'form-select'}),
            'des_nombre':forms.Select(attrs={'class':'form-select'}),
            'concentracion':forms.NumberInput(attrs={'max_length': '2','class':'form-control'}),
            'tiempo_inicio':forms.TimeInput(attrs={'type':'time'}),
            'tiempo_fin':forms.TimeInput(attrs={'type':'time'}),
            'obsevacion':forms.Textarea(attrs={'placeholder': 'Escriba su observacion','class':'form-control'})    
            } 
        
class DesinfeccionMPUpdateForm(forms.ModelForm):

    class Meta:

        model = Desinfeccion
        fields=(
            'mp_lote',
            'des_nombre',
            'concentracion',
            'tiempo_inicio',
            'tiempo_fin',
            'obsevacion', 
             
        )

        widgets={
            'mp_lote':forms.Select(attrs={'class':'form-select'}),
            'des_nombre':forms.Select(attrs={'class':'form-select'}),
            'concentracion':forms.NumberInput(attrs={'max_length': '2','class':'form-control'}),
            'tiempo_inicio':forms.TimeInput(attrs={'type':'time'}),
            'tiempo_fin':forms.TimeInput(attrs={'type':'time'}),
            'obsevacion':forms.Textarea(attrs={'placeholder': 'Escriba su observacion','class':'form-control'})    
            }     

class DesinfectanteGenericoForm(forms.ModelForm):

    class Meta:

        model = DesinfectanteGenerico
        fields=(
            'des_nombre',
        )

        widgets={
            'des_nombre':forms.TextInput(attrs={'class':'form-control'}),
            } 

class MateriaAuditFilterForm(forms.Form):
    '''Formulario para filtar en MateriaAuditListView'''
    user = forms.ModelChoiceField(queryset=MateriaPrima.objects.all(), 
                                  required=False, 
                                  label='Materia Prima Afectada',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    action = forms.ChoiceField(choices=MateriaPrimaAudit.ACTION_CHOICES, 
                               required=False, 
                               label='Acción',
                               widget=forms.Select(attrs={'class': 'form-select'}))
    changed_by = forms.ModelChoiceField(queryset=User.objects.all(), 
                                        required=False, 
                                        label='Cambios realizados por',
                                        widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField(label='Fecha inicial', 
                                 required=False, 
                                 widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    end_date = forms.DateField(label='Fecha final', 
                               required=False, 
                               widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))


