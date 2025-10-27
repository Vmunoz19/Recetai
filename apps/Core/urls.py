from django.urls import path
from .views import home_view, recipes_view, recipe_detail_view, ingredient_recognition_view, ingredient_recognition_results_view, saved_recipes_view
from .views import home_view, recipes_view, recipe_detail_view, ingredient_recognition_view, ingredient_recognition_results_view, saved_recipes_view
from .views.recipe_views import toggle_favorite_view
from .views.ingredient_api import detect_ingredients_api

app_name = 'core'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('recipes/', recipes_view, name='recipes'),
    path('recipe/<int:pk>/', recipe_detail_view, name='recipe_detail'),
    path('ingredients/', ingredient_recognition_view, name='ingredient_recognition'),
    path('ingredients/results/', ingredient_recognition_results_view, name='ingredient_recognition_results'),
    path('ingredients/api/detect/', detect_ingredients_api, name='api_vision_detect'),
    path("saved/", saved_recipes_view, name="saved_recipes"),
    path('recipe/<int:pk>/favorite/', toggle_favorite_view, name='toggle_favorite'),
]
