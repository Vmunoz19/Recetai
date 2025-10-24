from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.security.forms.profile_forms import ProfileForm


@login_required
def profile_view(request):
    """
    Vista para mostrar y actualizar el perfil del usuario
    """
    if request.method == 'POST':
        print("=== POST Request Recibido ===")
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        if form.is_valid():
            user = form.save()
            print("Usuario guardado:", user.first_name, user.last_name)
            # Refrescar el usuario desde la base de datos
            user.refresh_from_db()
            
            # Si es una petición AJAX, retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Perfil actualizado correctamente',
                    'user': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'phone_number': user.phone_number or '',
                        'national_id': user.national_id or '',
                        'address': user.address or '',
                        'city': user.city or '',
                        'gender': user.gender or '',
                        'profile_photo': user.profile_photo.url if user.profile_photo else None,
                    }
                })
            
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('security:profile')
        else:
            # Si hay errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error al actualizar el perfil',
                    'errors': form.errors
                }, status=400)
            
            messages.error(request, 'Error al actualizar el perfil')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'security/profile.html', {
        'form': form,
        'user': request.user
    })
