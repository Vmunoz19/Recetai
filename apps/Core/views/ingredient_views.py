from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ingredient_recognition_view(request):
    """Vista de la pantalla de carga de imagen / escaneo"""
    
    return render(request, 'core/ingredients/ingredient_scan.html')


@login_required
def ingredient_recognition_results_view(request):
    """Vista de la pantalla de resultados del análisis de ingredientes"""
    
    # Datos quemados - listos para reemplazar con lógica real de IA
    detected_ingredients = [
        {'id': 1, 'name': 'Tomates'},
        {'id': 2, 'name': 'Albahaca'},
        {'id': 3, 'name': 'Ajo'},
        {'id': 4, 'name': 'Cebolla'},
        {'id': 5, 'name': 'Aceite de oliva'},
        {'id': 6, 'name': 'Sal'},
        {'id': 7, 'name': 'Pimienta'},
        {'id': 8, 'name': 'Pasta'},
    ]
    
    matching_recipes = [
        {
            'id': 1,
            'name': 'Tortilla Española Clásica',
            'image': 'https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=400&h=300&fit=crop',
            'time': 20,
            'match_percentage': 85,
            'matched_ingredients': ['Huevos', 'Cebolla'],
            'additional_count': 1,
        },
        {
            'id': 2,
            'name': 'Ensalada Mediterránea',
            'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop',
            'time': 15,
            'match_percentage': 92,
            'matched_ingredients': ['Tomates', 'Aceitunas'],
            'additional_count': 1,
        },
        {
            'id': 3,
            'name': 'Pasta con Ajo y Albahaca',
            'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=300&fit=crop',
            'time': 25,
            'match_percentage': 78,
            'matched_ingredients': ['Ajo', 'Albahaca'],
            'additional_count': 1,
        },
    ]
    
    # La receta generada con IA se mostrará solo cuando el usuario presione el botón
    # Los datos están hardcodeados en el template y aparecen con JavaScript
    
    context = {
        'detected_ingredients': detected_ingredients,
        'matching_recipes': matching_recipes,
    }
    
    return render(request, 'core/ingredients/ingredient_results.html', context)
