from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms.auth_forms import LoginForm, RegisterForm


def login_view(request):
    """Vista para el inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Verificar si el usuario marcó "Recordarme"
                remember_me = request.POST.get('remember')
                
                # Iniciar sesión del usuario
                login(request, user)
                
                # Si NO marcó "Recordarme", la sesión expira al cerrar el navegador
                # Si SÍ marcó "Recordarme", la sesión dura 2 semanas (1209600 segundos)
                if not remember_me:
                    request.session.set_expiry(0)  # Expira al cerrar el navegador
                else:
                    request.session.set_expiry(1209600)  # 2 semanas
                
                messages.success(request, f'¡Bienvenido de vuelta, {user.get_display_name()}!')
                return redirect('core:home')
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = LoginForm()
    
    return render(request, 'security/login.html', {'form': form})


def register_view(request):
    """Vista para el registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_display_name()}! Tu cuenta ha sido creada exitosamente.')
                return redirect('core:home')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al crear la cuenta. Por favor, intenta nuevamente.')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegisterForm()
    
    return render(request, 'security/register.html', {'form': form})


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('security:login')
