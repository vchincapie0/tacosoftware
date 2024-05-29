import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from applications.productoterminado.models import ProductoTerminadoGenerico
from .models import Picado, Coccion, Equipos

class SelectProductoTerminado(forms.ModelForm):
    class Meta:
        model = ProductoTerminadoGenerico
        fields = ('pt_nombre',)
        widgets={'pt_nombre':forms.Select(
            attrs={'class':'form-select'}
        )}

class PicadoForm(forms.ModelForm):

    """Form definition Picado."""

    class Meta:
        """Meta definition Picadoform."""

        model = Picado
        fields = (
            'pica_cantidad_total',
            'pica_pesoPostProcesamiento',
            'pica_merma',
            'pica_check',
            )
         
# class PicadoUpdateForm(forms.ModelForm):
#     """Form Update Picado."""
#     class Meta:

#         model =Picado
#         fields = [
#             'pica_nombre',
#             'pica_cantidad',
#             'pica_pesoMPposproceso',
#             'pica_merma'
            
#             ]

#         widgets={
#             'pica_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Producto','class': 'form-select'}),
#             'pica_cantidad':forms.NumberInput(attrs={'placeholder': 'Peso ','class': 'form-control'}),
#             'pica_pesoMPposproceso':forms.NumberInput(attrs={'placeholder': 'Peso Post Proceso','class': 'form-control'}),
#             'pica_merma':forms.NumberInput(attrs={'placeholder': 'Peso Merma','class': 'form-control'}),
#             'pica_check':forms.Select(attrs={'class': 'form-select'}),
#         }
    
#     def clean_pica_nombre(self):
#         nombre = self.cleaned_data['pica_nombre']
#         if not re.match("^[a-zA-Z ]+$", nombre):
#             raise forms.ValidationError("El nombre no debe contener números o caracteres especiales.")
#         return nombre
    

#     def clean_pica_cantidad(self):
#         cantidad = self.cleaned_data['pica_cantidad']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_proces_pesoPostProceso(self):
#         cantidad = self.cleaned_data['pica_pesoMPposproceso']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_pica_merma(self):
#         cantidad = self.cleaned_data['pica_merma']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad


# class addCoccion(forms.ModelForm):

#     """Form definition coccion."""

#     class Meta:
#         """Meta definition Coccionform."""

#         model = Coccion
#         fields = (
            
#             'cocc_nombre',
#             'cocc_cantidad',
#             'cocc_pesoMPposproceso',
#             'cocc_merma',
#             'cocc_tiempoCoccion',
#             'cocc_temperaturafinal',
#             'cocc_check',
#             )
        
#         widgets={
            
            
#             'cocc_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Producto','class': 'form-select'}),
#             'cocc_cantidad':forms.NumberInput(attrs={'placeholder': 'Peso ','class': 'form-select'}),
#             'cocc_pesoMPposproceso':forms.NumberInput(attrs={'placeholder': 'Peso Post Proceso','class': 'form-select'}),
#             'cocc_merma':forms.NumberInput(attrs={'placeholder': 'Peso Merma','class': 'form-select'}),
#             'cocc_tiempoCoccion':forms.TimeInput(attrs={'placeholder':'tiempo de coccion','class': 'form-select'}),
#             'cocc_temperaturafinal':forms.NumberInput(attrs={'placeholder':'Temperatura Final','class': 'form-select'}),
#             'cocc_check':forms.Select(attrs={'class': 'form-select'}),
#         }

#     def clean_cocc_nombre(self):
#         nombre = self.cleaned_data['cocc_nombre']
#         if not re.match("^[a-zA-Z ]+$", nombre):
#             raise forms.ValidationError("El nombre no debe contener números o caracteres especiales.")
#         return nombre
    

#     def clean_cocc_cantidad(self):
#         cantidad = self.cleaned_data['cocc_cantidad']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_cocc_pesoMPposproceso(self):
#         cantidad = self.cleaned_data['cocc_pesoMPposproceso']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_cocc_merma(self):
#         cantidad = self.cleaned_data['cocc_merma']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
# class CoccionUpdateForm(forms.ModelForm):
#     """Form Update Coccion."""
#     class Meta:

#         model =Coccion
#         fields = [
#             'cocc_nombre',
#             'cocc_cantidad',
#             'cocc_pesoMPposproceso',
#             'cocc_merma',
#             'cocc_tiempoCoccion',
#             'cocc_temperaturafinal',
#             'cocc_check',
#             ]

#         widgets={
#             'cocc_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Producto','class': 'form-select'}),
#             'cocc_cantidad':forms.NumberInput(attrs={'placeholder': 'Peso ','class': 'form-control'}),
#             'cocc_pesoMPposproceso':forms.NumberInput(attrs={'placeholder': 'Peso Post Proceso','class': 'form-control'}),
#             'cocc_merma':forms.NumberInput(attrs={'placeholder': 'Peso Merma','class': 'form-control'}),
#             'cocc_tiempoCoccion':forms.TimeInput(attrs={'placeholder':'tiempo de coccion','class': 'form-select'}),
#             'cocc_temperaturafinal':forms.NumberInput(attrs={'placeholder':'Temperatura Final','class': 'form-select'}),
#             'cocc_check':forms.Select(attrs={'class': 'form-select'}),
#         }

#     def clean_cocc_nombre(self):
#         nombre = self.cleaned_data['cocc_nombre']
#         if not re.match("^[a-zA-Z ]+$", nombre):
#             raise forms.ValidationError("El nombre no debe contener números o caracteres especiales.")
#         return nombre
    

#     def clean_cocc_cantidad(self):
#         cantidad = self.cleaned_data['cocc_cantidad']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_cocc_pesoMPposproceso(self):
#         cantidad = self.cleaned_data['cocc_pesoMPposproceso']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad
    
#     def clean_cocc_merma(self):
#         cantidad = self.cleaned_data['cocc_merma']
#         if cantidad <= 0:
#             raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
#         return cantidad

class addEquipos(forms.ModelForm):

    """Form Update Equipos."""

    class Meta:
        """Meta definition Equiposform."""

        model = Equipos
        fields = (
            'equi_encargadoCocina',
            'equi_encargadoEntrega',
            'equi_calidad',
            'equi_nombre',
            'equi_check',
            )
        
        widgets={
            'equi_encargadoCocina':forms.TextInput(attrs={'placeholder': 'Nombre del operario','class': 'form-select'}),
            'equi_encargadoEntrega':forms.TextInput(attrs={'placeholder': 'a quien entrega ','class': 'form-select'}),
            'equi_calidad':forms.Select(attrs={'class': 'form-select'}),
            'equi_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Equipo','class': 'form-control'}),
            'equi_check':forms.Select(attrs={'class': 'form-select'}),
            
        }
        
class EquiposUpdateForm(forms.ModelForm):

    """Form definition Equipos."""

    class Meta:

        model = Equipos
        fields = (
            'equi_encargadoCocina',
            'equi_encargadoEntrega',
            'equi_calidad',
            'equi_nombre',
            'equi_check',
            )
        
        widgets={
            'equi_encargadoCocina':forms.TextInput(attrs={'placeholder': 'Nombre del operario','class': 'form-select'}),
            'equi_encargadoEntrega':forms.TextInput(attrs={'placeholder': 'a quien entrega ','class': 'form-select'}),
            'equi_calidad':forms.Select(attrs={'class': 'form-select'}),
            'equi_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Equipo','class': 'form-control'}),
            'equi_check':forms.Select(attrs={'class': 'form-select'}),
            
        }