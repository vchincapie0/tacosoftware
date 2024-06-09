# Fecha de Creación: 16/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 08/05/2024

import re
from django import forms
from django.core.exceptions import ValidationError
# Importación de modelos
from .models import Proveedores, ProveedoresAudit
from applications.users.models import User

class ProveedorCreateForm(forms.ModelForm):
    """Formulario para la creación de proveedores."""

    class Meta:
        model = Proveedores
        fields = (
            'nit',
            'prov_nombre',
            'prov_telefono',
        )

        widgets = {
            'nit': forms.NumberInput(attrs={'class': 'form-control'}),
            'prov_nombre': forms.TextInput(attrs={'placeholder': 'Nombre del Proveedor', 'class': 'form-control'}),
            'prov_telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'type': 'number', 'class': 'form-control'}),
        }

    def clean_prov_telefono(self):
        '''Función que valida que el teléfono del proveedor tenga exactamente 10 dígitos.'''
        cantidad = self.cleaned_data['prov_telefono']
        if len(cantidad) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")
        elif len(cantidad) > 10:
            raise forms.ValidationError("El teléfono no debe tener más de 10 dígitos.")
        return cantidad
    
    def clean_prov_nombre(self):
        '''Función que valida que el nombre del proveedor no contenga caracteres especiales.'''
        nombre = self.cleaned_data['prov_nombre']
        if not re.match("^[a-zA-Z ]+$", nombre):
            raise forms.ValidationError("El nombre no debe contener números o caracteres especiales.")
        return nombre

class ProveedoresUpdateForm(forms.ModelForm):
    """Formulario para la actualización de proveedores."""

    class Meta:
        model = Proveedores
        fields = ['nit', 'prov_nombre', 'prov_telefono']

        widgets = {
            'nit': forms.NumberInput(attrs={'class': 'form-control'}),
            'prov_nombre': forms.TextInput(attrs={'placeholder': 'Nombre del Proveedor', 'class': 'form-control'}),
            'prov_telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'type': 'number', 'class': 'form-control'}),
        }

    def clean_prov_telefono(self):
        '''Función que valida que el teléfono del proveedor tenga exactamente 10 dígitos.'''
        cantidad = self.cleaned_data['prov_telefono']
        if len(cantidad) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")
        elif len(cantidad) > 10:
            raise forms.ValidationError("El teléfono no debe tener más de 10 dígitos.")
        return cantidad
    
    def clean_prov_nombre(self):
        '''Función que valida que el nombre del proveedor no contenga caracteres especiales.'''
        nombre = self.cleaned_data['prov_nombre']
        if not re.match("^[a-zA-Z ]+$", nombre):
            raise forms.ValidationError("El nombre no debe contener números o caracteres especiales.")
        return nombre

class ProveedorAuditFilterForm(forms.Form):
    '''Formulario para filtrar en la vista de auditoría de proveedores.'''
    
    proveedor = forms.ModelChoiceField(
        queryset=Proveedores.objects.all(), 
        required=False, 
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    action = forms.ChoiceField(
        choices=ProveedoresAudit.ACTION_CHOICES, 
        required=False, 
        label='Acción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    changed_by = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        label='Cambios realizados por',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        label='Fecha inicial', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='Fecha final', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
