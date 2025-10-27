from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from apps.Core.models import Receta, RecetaIngrediente

def ingredient_recognition_view(request):
    """Página pública para capturar/escaneo de ingredientes.
    Se dejó pública para que la cámara funcione sin necesidad de login.
    """
    return render(request, "core/ingredients/ingredient_scan.html")


def ingredient_recognition_results_view(request):
    """
    Resultado de reconocimiento: ejemplo base.
    Reemplaza 'detected_ingredients' con lo que te devuelva la IA.
    """
    # TODO: reemplazar por salida real de la IA
    detected_ingredients = ["ajo", "tomate"]  # ejemplo

    # Recetas que contengan al menos uno de los ingredientes detectados
    query = Q()
    for name in detected_ingredients:
        query |= Q(ingredientes__nombre_singular__icontains=name)

    matching_recipes = (
        Receta.objects.filter(query).distinct()
        .select_related("dificultad", "pais")
        .prefetch_related("categorias")
        .order_by("nombre")[:20]
    )

    context = {
        "detected_ingredients": detected_ingredients,
        "matching_recipes": matching_recipes,
    }
    return render(request, "core/ingredients/ingredient_results.html", context)
