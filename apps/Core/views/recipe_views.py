from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.Core.models import (
    Receta,
    RecetaIngrediente,
    PasoInstruccion,
    RecetaFavorita,
    Categoria,
    Dificultad,
)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from urllib.parse import urlencode

@ensure_csrf_cookie
@login_required
def recipes_view(request):
    # Parámetros de búsqueda y filtrado (GET)
    q = request.GET.get("q", "").strip()
    porciones_param = request.GET.get("porciones", "").strip()
    min_duration_param = request.GET.get("min_duration", "").strip()
    max_duration_param = request.GET.get("max_duration", "").strip()
    dificultad_param = request.GET.get("dificultad", "").strip()
    categoria_param = request.GET.get("categoria", "").strip()

    recetas = Receta.objects.all().select_related("pais", "dificultad").prefetch_related("categorias")

    # Búsqueda por nombre/descripcion (no exacta)
    if q:
        recetas = recetas.filter(nombre__icontains=q)

    # Filtrado por porciones (entero)
    porciones = None
    if porciones_param:
        try:
            porciones = int(porciones_param)
            recetas = recetas.filter(porciones=porciones)
        except ValueError:
            messages.error(request, "El campo 'porciones' debe ser un número entero.")

    # Filtrado por duración (intervalo)
    min_duration = None
    max_duration = None
    if min_duration_param:
        try:
            min_duration = int(min_duration_param)
            recetas = recetas.filter(duracion__gte=min_duration)
        except ValueError:
            messages.error(request, "La duración mínima debe ser un número entero.")
    if max_duration_param:
        try:
            max_duration = int(max_duration_param)
            recetas = recetas.filter(duracion__lte=max_duration)
        except ValueError:
            messages.error(request, "La duración máxima debe ser un número entero.")

    # Filtrado por dificultad
    dificultad = None
    if dificultad_param:
        try:
            dificultad = int(dificultad_param)
            recetas = recetas.filter(dificultad_id=dificultad)
        except ValueError:
            # puede ser que se pase el nombre en vez del id; intentamos filtrar por nivel
            recetas = recetas.filter(dificultad__nivel__icontains=dificultad_param)

    # Filtrado por categoría (id)
    categoria = None
    if categoria_param:
        try:
            categoria = int(categoria_param)
            recetas = recetas.filter(categorias__id=categoria)
        except ValueError:
            recetas = recetas.filter(categorias__nombre__icontains=categoria_param)

    # Evitar duplicados por join
    recetas = recetas.distinct()

    paginator = Paginator(recetas, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # IDs de recetas que el usuario ya marcó como favoritas
    favorite_ids = set(
        RecetaFavorita.objects.filter(usuario=request.user).values_list("receta_id", flat=True)
    )

    # Listas para los filtros (poblar selects)
    categorias = Categoria.objects.all().order_by('nombre')
    dificultades = Dificultad.objects.all().order_by('nivel')

    # Querystring actual (sin page) para paginación preservando filtros
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    querystring = params.urlencode()

    context = {
        "recipes": page_obj,
        "q": q,
        "favorite_ids": favorite_ids,
        "categorias": categorias,
        "dificultades": dificultades,
        # Valores seleccionados (para rellenar el formulario)
        "selected_porciones": porciones_param,
        "selected_min_duration": min_duration_param,
        "selected_max_duration": max_duration_param,
        "selected_dificultad": dificultad_param,
        "selected_categoria": categoria_param,
        "querystring": querystring,
    }
    return render(request, "core/recipes/recipes.html", context)

@ensure_csrf_cookie
@login_required
def recipe_detail_view(request, pk):
    receta = get_object_or_404(Receta, id=pk)
    # IMPORTANTE: pasar si ya es favorita para pintar el botón
    is_favorite = RecetaFavorita.objects.filter(
        usuario=request.user, receta=receta
    ).exists()

    context = {
        "receta": receta,
        "is_favorite": is_favorite,
        # ... tu contexto existente
    }
    return render(request, "core/recipes/recipe_detail.html", context)

@require_POST
def toggle_favorite_view(request, pk):
    """Alterna el favorito para la receta.

    Responde JSON y, si el usuario no está autenticado, devuelve 401 en vez
    de redirigir a la página de login (útil para peticiones AJAX).
    """
    # Verificar autenticación manualmente para que AJAX reciba 401 en vez de redirect
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "not_authenticated"}, status=401)

    receta = get_object_or_404(Receta, id=pk)

    try:
        fav, created = RecetaFavorita.objects.get_or_create(
            usuario=request.user,
            receta=receta,
        )
        if created:
            is_favorite = True
        else:
            # ya existía, así que se quita
            fav.delete()
            is_favorite = False

        return JsonResponse({
            "ok": True,
            "is_favorite": is_favorite,
            "recipe_id": receta.id,
        })
    except Exception as e:
        # Capturar errores inesperados y devolver JSON (para debugging)
        return JsonResponse({"ok": False, "error": str(e)}, status=500)