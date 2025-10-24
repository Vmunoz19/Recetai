from django import forms
from apps.security.models import CustomUser


class ProfileForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario
    """
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name', 
            'profile_photo',
            'phone_number',
            'national_id',
            'address',
            'city',
            'gender'
        ]
        exclude = ['email']  # Excluir explícitamente el email
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu apellido'
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 0999999999'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Número de cédula'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu dirección'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu ciudad'
            }),
            'gender': forms.Select(
                choices=[
                    ('', 'Selecciona'),
                    ('M', 'Masculino'),
                    ('F', 'Femenino'),
                    ('Otro', 'Otro')
                ],
                attrs={
                    'class': 'form-input'
                }
            ),
        }
        
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'profile_photo': 'Foto de perfil',
            'phone_number': 'Teléfono',
            'national_id': 'Cédula',
            'address': 'Dirección',
            'city': 'Ciudad',
            'gender': 'Género',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar campo email solo para visualización (no se guardará)
        self.fields['email'] = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={
                'class': 'form-input form-input-readonly',
                'readonly': 'readonly'
            }),
            label='Correo electrónico'
        )
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.email
    
    def clean(self):
        cleaned_data = super().clean()
        # Remover el email del cleaned_data para que no interfiera
        if 'email' in cleaned_data:
            del cleaned_data['email']

        # Validar nombres y apellidos (solo letras y espacios)
        first_name = cleaned_data.get('first_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()
        if not first_name.replace(' ', '').isalpha():
            self.add_error('first_name', 'El nombre solo debe contener letras.')
        if not last_name.replace(' ', '').isalpha():
            self.add_error('last_name', 'El apellido solo debe contener letras.')

        # Validar teléfono (10 dígitos numéricos)
        phone = cleaned_data.get('phone_number', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            self.add_error('phone_number', 'El teléfono debe tener 10 dígitos numéricos.')

        # Validar ciudad y dirección (no vacíos)
        city = cleaned_data.get('city', '').strip()
        address = cleaned_data.get('address', '').strip()
        if not city:
            self.add_error('city', 'La ciudad es obligatoria.')
        if not address:
            self.add_error('address', 'La dirección es obligatoria.')

        # Validar género
        gender = cleaned_data.get('gender', '')
        if gender not in ['M', 'F', 'Otro']:
            self.add_error('gender', 'Selecciona un género válido.')

        # Validar cédula ecuatoriana
        dni = cleaned_data.get('national_id', '').strip()
        if dni:
            if not dni.isdigit() or len(dni) != 10 or not self.validar_cedula_ecuatoriana(dni):
                self.add_error('national_id', 'La cédula debe ser válida y de Ecuador (10 dígitos).')
        return cleaned_data

    @staticmethod
    def validar_cedula_ecuatoriana(cedula):
        # Algoritmo oficial de validación de cédula ecuatoriana
        if len(cedula) != 10 or not cedula.isdigit():
            return False
        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            return False
        digitos = [int(d) for d in cedula]
        total = 0
        for i in range(9):
            if i % 2 == 0:
                val = digitos[i] * 2
                if val > 9:
                    val -= 9
                total += val
            else:
                total += digitos[i]
        verificador = 10 - (total % 10) if total % 10 != 0 else 0
        return verificador == digitos[9]
