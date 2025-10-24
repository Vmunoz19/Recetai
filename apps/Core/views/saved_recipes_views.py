from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def saved_recipes_view(request):
    """Vista de recetas guardadas: favoritas e historial de IA"""
    
    # Datos quemados - Recetas Favoritas
    favorite_recipes = [
        {
            'id': 1,
            'name': 'Pasta Primavera con Vegetales',
            'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=300&fit=crop',
            'time': 25,
            'portions': 4,
            'difficulty': 'Fácil',
        },
        {
            'id': 2,
            'name': 'Ensalada César con Pollo',
            'image': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop',
            'time': 20,
            'portions': 2,
            'difficulty': 'Fácil',
        },
        {
            'id': 3,
            'name': 'Risotto de Champiñones',
            'image': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop',
            'time': 35,
            'portions': 4,
            'difficulty': 'Media',
        },
    ]
    
    # Datos quemados - Historial de IA (recetas generadas)
    ai_history = [
        {
            'id': 1,
            'name': 'Pasta Mediterránea con Ingredientes Frescos',
            'date': '24 oct, 09:26',
            'time': 30,
            'portions': 4,
        },
        {
            'id': 2,
            'name': 'Pasta Mediterránea con Ingredientes Frescos',
            'date': '24 oct, 11:12',
            'time': 30,
            'portions': 4,
        },
        {
            'id': 3,
            'name': 'Tacos de Pollo con Aguacate',
            'date': '23 oct, 18:45',
            'time': 25,
            'portions': 3,
        },
        {
            'id': 4,
            'name': 'Sopa de Verduras al Estilo Casero',
            'date': '23 oct, 14:20',
            'time': 40,
            'portions': 6,
        },
    ]
    
    context = {
        'favorite_recipes': favorite_recipes,
        'ai_history': ai_history,
    }
    
    return render(request, 'core/saved_recipes/saved_recipes.html', context)
