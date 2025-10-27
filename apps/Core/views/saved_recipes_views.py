from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from apps.Core.models import RecetaFavorita, HistorialRecetaGenerada, RecetaGenerada

@login_required
def saved_recipes_view(request):
    """
    Muestra las recetas favoritas del usuario y su historial de IA.
    Compatible con el template saved_recipes.html.
    """

    # Recetas favoritas del usuario
    favorite_recipes = [
        {
            "id": fav.receta.id,
            "name": fav.receta.nombre,
            "image": fav.receta.image_url,
            "time": fav.receta.duracion or 0,
            "portions": fav.receta.porciones or 1,
            "difficulty": fav.receta.dificultad.nivel if fav.receta.dificultad else "—",
        }
        for fav in RecetaFavorita.objects.select_related(
            "receta", "receta__dificultad"
        ).filter(usuario=request.user)
    ]

    # Historial de recetas generadas con IA
    ai_history = [
        {
            "name": item.receta_generada.nombre,
            "date": item.receta_generada.created_at.strftime("%d %b %Y") if hasattr(item.receta_generada, "created_at") else "",
            "time": item.receta_generada.duracion if hasattr(item.receta_generada, "duracion") else "",
            "portions": item.receta_generada.porciones if hasattr(item.receta_generada, "porciones") else "",
        }
        for item in HistorialRecetaGenerada.objects.select_related(
            "receta_generada"
        ).filter(usuario=request.user)
    ]

    context = {
        "favorite_recipes": favorite_recipes,
        "ai_history": ai_history,
    }

    return render(request, "core/saved_recipes/saved_recipes.html", context)