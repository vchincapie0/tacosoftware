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

class addEquipos(forms.ModelForm):

    """Form Update Equipos."""

    class Meta:
        """Meta definition Equiposform."""

        model = Equipos
        fields = (
            'equi_encargadoCocina',
            'equi_encargadoEntrega',
            'equi_nombre',
            'equi_check',
            )
        
        widgets={
            'equi_encargadoCocina':forms.Select(attrs={'placeholder': 'Nombre del operario','class': 'form-select'}),
            'equi_encargadoEntrega':forms.Select(attrs={'placeholder': 'a quien entrega ','class': 'form-select'}),
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
            'equi_nombre',
            'equi_check',
            )
        
        widgets={
            'equi_encargadoCocina':forms.Select(attrs={'placeholder': 'Nombre del operario','class': 'form-select'}),
            'equi_encargadoEntrega':forms.Select(attrs={'placeholder': 'a quien entrega ','class': 'form-select'}),
            'equi_nombre':forms.TextInput(attrs={'placeholder': 'Nombre del Equipo','class': 'form-control'}),
            'equi_check':forms.Select(attrs={'class': 'form-select'}),
            
        }