import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Insumos,InsumosGenerico,InsumosAudit
from applications.users.models import User

class InsumosGenericoForm(forms.ModelForm):
    class Meta:
        model = InsumosGenerico
        fields = (
            'it_nombre',
            )
        widgets={
            
            'it_nombre':forms.TextInput(attrs={'class':'form-control'}),
        }

class InsumosGenericoUpdateForm(forms.ModelForm):

    class Meta:
        model = InsumosGenerico
        fields = (
            'it_nombre',
            )
        widgets={
            'it_nombre':forms.TextInput(attrs={'class':'form-control'}),
            }
    
class InsumosUpdateForm(forms.ModelForm):
    """Form Update Insumos."""
    class Meta:

        model = Insumos
        fields = ['it_nombre', 'it_cantidad', 'it_fechaEntrega', 'it_estado']

        widgets={
            'it_nombre':forms.Select(attrs={'class':'form-select'}),
            'it_cantidad':forms.NumberInput(attrs={'placeholder': 'Cantidad Entregada','class':'form-control'}),
            'it_fechaEntrega':forms.SelectDateWidget(),
            'it_estado':forms.Select(attrs={'class':'form-select'})
        }
    
    def clean_it_cantidad(self):
        cantidad = self.cleaned_data['it_cantidad']
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser un número mayor que 0.")
        return cantidad

class InsumosAuditFilterForm(forms.Form):
    '''Formulario para filtar en insumosauditview'''

    user = forms.ModelChoiceField(queryset=Insumos.objects.all(), 
                                  required=False, 
                                  label='Implemento Afectado',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    action = forms.ChoiceField(choices=InsumosAudit.ACTION_CHOICES, 
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
    