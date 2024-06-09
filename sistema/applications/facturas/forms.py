# Fecha de Creación: 27/02/2024
# Última modificación: 11/05/2024

from django import forms
from .models import Facturas, IVA, FacturasAudit
from applications.users.models import User
from applications.proveedores.models import Proveedores
from applications.pedidos.models import Pedidos

#Autor: Kevin Dayann Albarracin Navarrete
class IVACreateForm(forms.ModelForm):
    '''Formulario para crear IVA'''
    class Meta:
        model =IVA
        fields = (
            'valor',
            )
        widgets={
            'valor':forms.NumberInput(attrs={'class':'form-control'}), 
        }

#Autor: Kevin Dayann Albarracin Navarrete
class IVAUpdateForm(forms.ModelForm):
    '''Formulario para editar IVA'''
    class Meta:
        model =IVA
        fields = (
            'valor',
            )
        widgets={
            'valor':forms.NumberInput(attrs={'class':'form-control'}), 
        }

#Autor:     
class FacturaCreateForm(forms.ModelForm):
    '''Formulario para crear facturas'''
    class Meta:
        model = Facturas
        fields = (
            'num_factura',
            'fac_proveedor',
            'fac_numeroPedido',
            'fac_fechaLlegada',
            'fac_numeroUnidades',
            'img_factura',
            'fac_subtotal',
            'fac_iva',
            )
        
        widgets={
            'num_factura':forms.NumberInput(attrs={'class':'form-control'}),
            'fac_proveedor':forms.Select(attrs={'class':'form-select'}),
            'fac_numeroPedido':forms.Select(attrs={'class':'form-select'}),
            'fac_fechaLlegada':forms.SelectDateWidget(),
            'fac_numeroUnidades':forms.NumberInput(attrs={'class':'form-control'}), 
            'img_factura':forms.FileInput(attrs={'class':'form-control'}),
            'fac_subtotal':forms.NumberInput(attrs={'class':'form-control','placeholder':'Subtotal'}),
            'fac_iva':forms.Select(attrs={'class':'form-select'}),
        }

#Autor: 
class FacturaUpdateForm(forms.ModelForm):
    '''Formulario para editar facturas'''
    class Meta:
        model = Facturas
        fields = (
            'num_factura',
            'fac_proveedor',
            'fac_numeroPedido',
            'fac_fechaLlegada',
            'fac_numeroUnidades',
            'img_factura',
            'fac_subtotal',
            'fac_iva',
            )
        
        widgets={
            'num_factura':forms.NumberInput(attrs={'class':'form-control'}),
            'fac_proveedor':forms.Select(attrs={'class':'form-select'}),
            'fac_numeroPedido':forms.Select(attrs={'class':'form-select'}),
            'fac_fechaLlegada':forms.SelectDateWidget(),
            'fac_numeroUnidades':forms.NumberInput(attrs={'class':'form-control'}), 
            'img_factura':forms.FileInput(attrs={'class':'form-control'}),
            'fac_subtotal':forms.NumberInput(attrs={'class':'form-control','placeholder':'Subtotal'}),
            'fac_iva':forms.Select(attrs={'class':'form-select'}),
        }

#Autor: Vivian Carolina Hincapie Escobar
class FacturasAuditFilterForm(forms.Form):
    '''Formulario para filtar en FacturasAuditView'''
    factura = forms.ModelChoiceField(
        queryset=Facturas.objects.all(), 
        required=False, 
        label='Factura',
        widget=forms.Select(
            attrs={'class': 'form-select'}))
    action = forms.ChoiceField(
        choices=FacturasAudit.ACTION_CHOICES, 
        required=False, 
        label='Acción',
        widget=forms.Select(
            attrs={'class': 'form-select'}))
    changed_by = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        label='Cambios realizados por',
        widget=forms.Select(
            attrs={'class': 'form-select'}))
    start_date = forms.DateField(
        label='Fecha inicial', 
        required=False, 
        widget=forms.DateInput(
            attrs={'type': 'date', 'class':'form-control'}))
    end_date = forms.DateField(
        label='Fecha final', 
        required=False, 
        widget=forms.DateInput(
            attrs={'type': 'date', 'class':'form-control'}))
    # Agregar campos de filtro para Pedido y Proveedor
    pedido = forms.ModelChoiceField(
        queryset=Pedidos.objects.all(),
        required=False,
        label='Pedido',
        widget=forms.Select(
            attrs={'class': 'form-select'})
    )
    proveedor = forms.ModelChoiceField(
        queryset=Proveedores.objects.all(),
        required=False,
        label='Proveedor',
        widget=forms.Select(
            attrs={'class': 'form-select'})
    )     