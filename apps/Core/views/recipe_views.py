from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def recipes_view(request):
    """Vista del listado de recetas"""
    # Datos quemados - listos para reemplazar con queryset desde BD
    recipes = [
        {
            'id': 1,
            'name': 'Pasta Primavera',
            'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=300&fit=crop',
            'rating': 4.5,
            'time': 30,
            'portions': 4,
            'difficulty': 'Fácil',
            'tags': ['Italiana', 'Vegetariana'],
        },
        {
            'id': 2,
            'name': 'Ensalada Mediterránea',
            'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop',
            'rating': 4.8,
            'time': 15,
            'portions': 2,
            'difficulty': 'Fácil',
            'tags': ['Saludable', 'Rápida'],
        },
        {
            'id': 3,
            'name': 'Tarta de Chocolate',
            'image': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop',
            'rating': 4.9,
            'time': 60,
            'portions': 8,
            'difficulty': 'Media',
            'tags': ['Postre', 'Especial'],
        },
    ]
    
    context = {
        'recipes': recipes,
    }
    return render(request, 'core/recipes/recipes.html', context)


@login_required
def recipe_detail_view(request, pk):
    """Vista del detalle de una receta"""
    # Datos quemados - listos para reemplazar con get_object_or_404(Recipe, pk=pk)
    recipes_data = {
        1: {
            'id': 1,
            'name': 'Pasta Primavera',
            'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600&h=400&fit=crop',
            'description': 'Una deliciosa pasta con vegetales frescos de temporada, perfecta para una comida ligera y nutritiva. Esta receta italiana combina los sabores del verano en cada bocado.',
            'rating': 4.5,
            'time': 30,
            'portions': 4,
            'difficulty': 'Fácil',
            'ingredients': [
                {'name': 'Pasta tipo penne', 'amount': '400g', 'icon': 'fa-wheat-awn'},
                {'name': 'Tomates cherry', 'amount': '200g', 'icon': 'fa-apple-whole'},
                {'name': 'Calabacín', 'amount': '1 unidad', 'icon': 'fa-leaf'},
                {'name': 'Pimiento rojo', 'amount': '1 unidad', 'icon': 'fa-pepper-hot'},
                {'name': 'Ajo', 'amount': '3 dientes', 'icon': 'fa-mortar-pestle'},
                {'name': 'Aceite de oliva', 'amount': '4 cdas', 'icon': 'fa-bottle-droplet'},
                {'name': 'Albahaca fresca', 'amount': 'al gusto', 'icon': 'fa-seedling'},
                {'name': 'Queso parmesano', 'amount': '100g', 'icon': 'fa-cheese'},
                {'name': 'Sal y pimienta', 'amount': 'al gusto', 'icon': 'fa-salt-shaker'},
            ],
            'instructions': [
                'Cocer la pasta en agua con sal según las instrucciones del paquete hasta que esté al dente.',
                'Mientras tanto, cortar todos los vegetales en trozos pequeños y uniformes.',
                'En una sartén grande, calentar el aceite de oliva y sofreír el ajo picado hasta que esté dorado.',
                'Añadir los vegetales cortados y saltear a fuego medio-alto durante 5-7 minutos.',
                'Escurrir la pasta reservando un poco del agua de cocción.',
                'Mezclar la pasta con los vegetales, añadiendo un poco del agua de cocción si es necesario.',
                'Servir caliente con albahaca fresca y queso parmesano rallado por encima.',
            ],
        },
        2: {
            'id': 2,
            'name': 'Ensalada Mediterránea',
            'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&h=400&fit=crop',
            'description': 'Fresca ensalada con ingredientes típicos del Mediterráneo.',
            'rating': 4.8,
            'time': 15,
            'portions': 2,
            'difficulty': 'Fácil',
            'ingredients': [
                {'name': 'Lechuga romana', 'amount': '1 unidad', 'icon': 'fa-leaf'},
                {'name': 'Tomate', 'amount': '2 unidades', 'icon': 'fa-apple-whole'},
                {'name': 'Pepino', 'amount': '1 unidad', 'icon': 'fa-leaf'},
                {'name': 'Aceitunas negras', 'amount': '100g', 'icon': 'fa-circle'},
                {'name': 'Queso feta', 'amount': '150g', 'icon': 'fa-cheese'},
            ],
            'instructions': [
                'Lavar y cortar todos los vegetales en trozos medianos.',
                'Colocar en un bowl grande y mezclar.',
                'Añadir las aceitunas y el queso feta desmenuzado.',
                'Aliñar con aceite de oliva, limón, sal y orégano.',
                'Servir inmediatamente bien frío.',
            ],
        },
        3: {
            'id': 3,
            'name': 'Tarta de Chocolate',
            'image': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&h=400&fit=crop',
            'description': 'Deliciosa tarta de chocolate con ganache suave y esponjoso bizcocho.',
            'rating': 4.9,
            'time': 60,
            'portions': 8,
            'difficulty': 'Media',
            'ingredients': [
                {'name': 'Chocolate negro', 'amount': '300g', 'icon': 'fa-square'},
                {'name': 'Mantequilla', 'amount': '200g', 'icon': 'fa-butter'},
                {'name': 'Azúcar', 'amount': '150g', 'icon': 'fa-cube'},
                {'name': 'Huevos', 'amount': '4 unidades', 'icon': 'fa-egg'},
                {'name': 'Harina', 'amount': '100g', 'icon': 'fa-wheat-awn'},
            ],
            'instructions': [
                'Precalentar el horno a 180°C.',
                'Derretir el chocolate con la mantequilla al baño maría.',
                'Batir los huevos con el azúcar hasta que estén espumosos.',
                'Incorporar el chocolate derretido a los huevos.',
                'Añadir la harina tamizada mezclando suavemente.',
                'Verter en un molde enmantequillado.',
                'Hornear durante 35-40 minutos.',
                'Dejar enfriar antes de desmoldar y servir.',
            ],
        },
    }
    
    recipe = recipes_data.get(pk, recipes_data[1])  # Default a la primera si no existe
    
    context = {
        'recipe': recipe,
    }
    return render(request, 'core/recipes/recipe_detail.html', context)
