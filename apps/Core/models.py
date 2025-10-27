from django.db import models
from apps.security import models as security
from django.conf import settings

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Ingrediente(models.Model):
    nombre_singular = models.CharField(max_length=100, unique=True)


class Dificultad(models.Model):
    nivel = models.CharField(max_length=50, unique=True)

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

class RecetaGenerada(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    categorias = models.ManyToManyField(Categoria, through='RecetaGeneradaCategoria')
    ingredientes = models.ManyToManyField(Ingrediente, through='RecetaGeneradaIngrediente')
    dificultad = models.ForeignKey(Dificultad, on_delete=models.SET_NULL, null=True)
    porciones = models.PositiveSmallIntegerField(default=2)
    descripcion = models.TextField(blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)


class Receta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    categorias = models.ManyToManyField(Categoria, through='RecetaCategoria')
    ingredientes = models.ManyToManyField(Ingrediente, through='RecetaIngrediente')
    image_url = models.TextField(blank=True, null=True)
    dificultad = models.ForeignKey(Dificultad, on_delete=models.SET_NULL, null=True)
    porciones = models.PositiveSmallIntegerField(default=2)
    duracion = models.PositiveIntegerField(help_text='Duración en minutos', null=True, blank=True)
    valoracion = models.DecimalField(max_digits=3, decimal_places=2, default=0)

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # ← cambio
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True)

class RecetaCategoria(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
class RecetaGeneradaIngrediente(models.Model):
    receta_generada = models.ForeignKey(RecetaGenerada, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True)

class RecetaGeneradaCategoria(models.Model):
    receta_generada = models.ForeignKey(RecetaGenerada, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class RecetaGeneradaFavorita(models.Model):
    usuario = models.ForeignKey(security.CustomUser, on_delete=models.CASCADE)
    receta_generada = models.ForeignKey('RecetaGenerada', on_delete=models.CASCADE)

class RecetaFavorita(models.Model):
    usuario = models.ForeignKey(security.CustomUser, on_delete=models.CASCADE)
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'receta')
        verbose_name = 'Receta Favorita'
        verbose_name_plural = 'Recetas Favoritas'

# 🔹 Historial de recetas generadas con IA (por usuario)
class HistorialRecetaGenerada(models.Model):
    usuario = models.ForeignKey(security.CustomUser, on_delete=models.CASCADE)
    receta_generada = models.ForeignKey('RecetaGenerada', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Historial de Receta Generada'
        verbose_name_plural = 'Historial de Recetas Generadas'

class PasoInstruccion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    orden = models.PositiveSmallIntegerField()
    texto = models.TextField()

class PasoInstruccionGenerada(models.Model):
    receta_generada = models.ForeignKey(RecetaGenerada, on_delete=models.CASCADE)
    orden = models.PositiveSmallIntegerField()
    texto = models.TextField()