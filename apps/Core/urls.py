from django.urls import path
from .views import home_view, recipes_view, recipe_detail_view, ingredient_recognition_view, ingredient_recognition_results_view, saved_recipes_view

app_name = 'core'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('recipes/', recipes_view, name='recipes'),
    path('recipe/<int:pk>/', recipe_detail_view, name='recipe_detail'),
    path('ingredients/', ingredient_recognition_view, name='ingredient_recognition'),
    path('ingredients/results/', ingredient_recognition_results_view, name='ingredient_recognition_results'),
    path('saved/', saved_recipes_view, name='saved_recipes'),
]
