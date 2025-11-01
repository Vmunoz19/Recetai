import unicodedata
import re
from typing import Set, List
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from apps.Core.models import Ingrediente

# Diccionario de traducción inglés -> español (ampliable)
EN_TO_ES = {
    "apple": "manzana",
    "banana": "plátano",
    "pear": "pera",
    "strawberry": "fresa",
    "mango": "mango",
    "pineapple": "piña",
    "grape": "uva",
    "orange": "naranja",
    "lemon": "limón",
    "melon": "melón",
    "watermelon": "sandía",
    "coconut": "coco",
    "papaya": "papaya",
    "kiwi": "kiwi",
    "raspberry": "frambuesa",
    "blueberry": "arándano",
    "peach": "durazno",
    "guava": "guayaba",
    "passion fruit": "maracuyá",
    "cherry": "cereza",
    "tomato": "tomate",
    "onion": "cebolla",
    "garlic": "ajo",
    "carrot": "zanahoria",
    "potato": "papa",
    "pepper": "pimiento",
    "bell pepper": "pimiento",
    "chili": "chile",
    "cucumber": "pepino",
    "spinach": "espinaca",
    "lettuce": "lechuga",
    "broccoli": "brócoli",
    "cauliflower": "coliflor",
    "zucchini": "calabacín",
    "eggplant": "berenjena",
    "celery": "apio",
    "corn": "maíz",
    "bean": "frijol",
    "chickpea": "garbanzo",
    "chicken": "pollo",
    "beef": "carne de res",
    "pork": "cerdo",
    "fish": "pescado",
    "egg": "huevo",
    "milk": "leche",
    "cheese": "queso",
    "butter": "mantequilla",
    "rice": "arroz",
    "bread": "pan",
    "sugar": "azúcar",
    "salt": "sal",
    "olive oil": "aceite de oliva",
}

STOPWORDS = {
    'gramos','g','ml','mililitros','litro','litros','taza','tazas','cucharada','cucharadas',
    'sopera','postre','mitad','media','libra','libras','paquete','atado','copita','chorro',
    'botella','bote','sobre','sobres','centimetros','cm','cubicos','cc','kilogramo',
    'kilogramos','kg','barra','barras','puñado','medio','y','de','el','la','los','las',
    'al','del','a','s','(s)'
}

def _strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def _normalize_token_stream(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü\s]', ' ', text)
    tokens = [t for t in text.split() if t and t not in STOPWORDS]
    return tokens

def normalizar_ingrediente(nombre: str) -> str:
    if not nombre:
        return ""
    txt = nombre.strip().lower()
    # quitar acentos
    txt_no_acc = _strip_accents(txt)
    tokens = _normalize_token_stream(txt_no_acc)
    return " ".join(tokens).strip()

def _candidates_from_label_en(label_en: str) -> Set[str]:
    out: Set[str] = set()
    if not label_en:
        return out
    k = label_en.strip().lower()
    if k in EN_TO_ES:
        out.add(EN_TO_ES[k])
    out.add(k)
    return {normalizar_ingrediente(x) for x in out if x}

def map_label_to_db_candidates(raw_label: str) -> List[str]:
    return sorted(list(_candidates_from_label_en(raw_label)))

def buscar_en_bd(candidates: List[str]):
    """
    Busca ingredientes coincidentes usando similitud trigram y fallback icontains.
    Evita usar union() para compatibilidad total.
    """
    from apps.Core.models import Ingrediente
    if not candidates:
        return Ingrediente.objects.none()

    ids = set()

    # Trigram primero
    for c in candidates:
        if not c:
            continue
        for ing in Ingrediente.objects.annotate(sim=TrigramSimilarity('nombre_singular', c)).filter(sim__gt=0.30):
            ids.add(ing.id)

    # Fallback icontains con y sin acentos
    for c in candidates:
        if not c:
            continue
        for ing in Ingrediente.objects.filter(nombre_singular__icontains=c):
            ids.add(ing.id)
        for ing in Ingrediente.objects.filter(nombre_singular__icontains=_strip_accents(c)):
            ids.add(ing.id)

    return Ingrediente.objects.filter(id__in=list(ids))
