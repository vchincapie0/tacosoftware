from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from . models import User, UserAudit

class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""

    password=forms.CharField(
        label='Contraseña:',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Contraseña','class':'form-control'}
        ),
    )

    password2=forms.CharField(
        label='Repetir contraseña:',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Contraseña','class':'form-control'}
        )
    )

    class Meta:
        """Meta definition for UserRegisterform."""

        model = User
        fields = ('username',
                  'name',
                  'last_name',
                  'is_admin',)
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Ejemplo: mperez22'}),
            'name':forms.TextInput(attrs={'placeholder': 'Ejemplo: María','class':'form-control'}),
            'last_name':forms.TextInput(attrs={'placeholder': 'Ejemplo: Perez','class':'form-control'}),
            'is_admin':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
                  
        
    def clean_username(self):
        '''Función para validar si el usuario ya existe'''
        username = self.cleaned_data.get('username')

        # Verificar si ya existe un usuario con el mismo nombre de usuario
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')

        return username
        

    def clean_password(self):
        '''Funcion para validar que las contraseñas tenga > 6 caracteres'''
        contraseña = self.cleaned_data.get('password')

        if len(contraseña) <= 5:
            self.add_error('password','La contraseña debe tener más de 5 caracteres.')
        
        return contraseña

    def clean_password2(self):
        '''Funcion para validar que las contraseñas coincidan'''
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password2','Las contraseñas no coinciden.')

    def clean_name(self):
        '''Función para validar el campo de nombre'''
        name = self.cleaned_data.get('name')

        if any(char.isdigit() or not char.isalpha() for char in name):
            raise ValidationError('El nombre solo puede contener letras.')

        return name
    
    def clean_last_name(self):
        '''Función para validar el campo de apellido'''
        last_name = self.cleaned_data.get('last_name')

        if any(char.isdigit() or not char.isalpha() for char in last_name):
            raise ValidationError('El apellido solo puede contener letras.')

        return last_name
    
class UserUpdateForm(forms.ModelForm):
    '''Clase de formulario para editar un usuario'''
    password=forms.CharField(
            label='Contraseña:',
            required=False,
            widget=forms.PasswordInput(
                attrs={'placeholder':'Contraseña Nueva','class':'form-control'}
            )
        )    

    password2=forms.CharField(
        label='Repetir contraseña:',
            required=False,
            widget=forms.PasswordInput(
                attrs={'placeholder':'Repetir Contraseña Nueva','class':'form-control'}
            )
        ) 

    class Meta:
        model = User
        fields = ['username', 'name', 'last_name', 'is_admin',]
    
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control-plaintext text-light','readonly':'True'}),
            'name':forms.TextInput(attrs={'placeholder': 'Ejemplo: María','class':'form-control'}),
            'last_name':forms.TextInput(attrs={'placeholder': 'Ejemplo: Perez','class':'form-control'}),
            'is_admin':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:
            if len(password) <= 5:
                raise ValidationError('La contraseña debe tener más de 5 caracteres.')

        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('Las contraseñas no coinciden.')

        return password2

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if any(char.isdigit() or not char.isalpha() for char in name):
            raise ValidationError('El nombre solo puede contener letras.')

        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if any(char.isdigit() or not char.isalpha() for char in last_name):
            raise ValidationError('El apellido solo puede contener letras.')

        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and not password2:
            raise ValidationError('Debes repetir la nueva contraseña.')

        return cleaned_data

class UserAuditFilterForm(forms.Form):
    '''Formulario para filtar en userauditview'''
    user = forms.ModelChoiceField(queryset=User.objects.all(), 
                                  required=False, 
                                  label='Usuario Afectado',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    action = forms.ChoiceField(choices=UserAudit.ACTION_CHOICES, 
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