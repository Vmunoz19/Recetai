from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from ..models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'tu@email.com',
        }),
        label='Correo electrónico',
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingresa un correo electrónico válido.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
        }),
        label='Contraseña',
        error_messages={
            'required': 'La contraseña es obligatoria.',
        }
    )
    
    error_messages = {
        'invalid_login': 'Correo electrónico o contraseña incorrectos.',
        'inactive': 'Esta cuenta está inactiva.',
    }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input register-focus',
            'placeholder': 'Tu nombre',
        }),
        label='Nombre',
        error_messages={
            'required': 'El nombre es obligatorio.',
            'max_length': 'El nombre no puede tener más de 150 caracteres.',
        }
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input register-focus',
            'placeholder': 'Tu apellido',
        }),
        label='Apellido',
        error_messages={
            'required': 'El apellido es obligatorio.',
            'max_length': 'El apellido no puede tener más de 150 caracteres.',
        }
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input register-focus',
            'placeholder': 'tu@email.com',
        }),
        label='Correo electrónico',
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingresa un correo electrónico válido.',
        }
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input register-focus',
            'placeholder': '••••••••',
        }),
        label='Contraseña',
        error_messages={
            'required': 'La contraseña es obligatoria.',
        },
        help_text='Tu contraseña debe tener al menos 8 caracteres.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input register-focus',
            'placeholder': '••••••••',
        }),
        label='Confirmar contraseña',
        error_messages={
            'required': 'Debes confirmar tu contraseña.',
        }
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de error de password1 en español
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
