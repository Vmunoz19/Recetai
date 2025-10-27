import unicodedata
from typing import Set, List

# Diccionario de traducción inglés -> español (básico, ampliable)
EN_TO_ES = {
    'tomato': ['tomate'],
    'potato': ['patata', 'papa'],
    'onion': ['cebolla'],
    'garlic': ['ajo'],
    'carrot': ['zanahoria'],
    'lettuce': ['lechuga'],
    'cucumber': ['pepino'],
    'egg': ['huevo'],
    'milk': ['leche'],
    'cheese': ['queso'],
    'chicken': ['pollo'],
    'beef': ['carne', 'carne de res'],
    'pork': ['cerdo'],
    'mushroom': ['champiñón', 'hongo'],
    'apple': ['manzana'],
    'banana': ['platano', 'banana', 'banano'],
    'orange': ['naranja'],
    'strawberry': ['fresa', 'frutilla'],
    'grape': ['uva'],
    'avocado': ['aguacate'],
    'rice': ['arroz'],
    'pasta': ['pasta'],
    'pepper': ['pimiento'],
    'chili': ['aji', 'chile', 'guindilla'],
    'lemon': ['limon'],
    'lime': ['lima'],
    'pineapple': ['piña'],
}

# Sinónimos / variantes (puedes ampliarlo)
SYNONYMS = {
    'tomato': ['tomatoes', 'tomatillo'],
    'potato': ['potatoes', 'papa'],
    'banana': ['bananas', 'plantain'],
    'egg': ['eggs'],
    'cheese': ['quesos'],
}


def _strip_accents(text: str) -> str:
    nk = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nk if not unicodedata.combining(c)])


def _singularize_en(word: str) -> str:
    # heurística simple: quita 'es' o 's' al final si parece plural
    if word.endswith('ies'):
        return word[:-3] + 'y'
    if word.endswith('es'):
        return word[:-2]
    if word.endswith('s') and len(word) > 3:
        return word[:-1]
    return word


def generate_label_candidates(raw_label: str) -> Set[str]:
    """Genera un conjunto de candidatos (ingles/español/sinónimos/normalizados)

    Ejemplo: 'Tomatoes' -> {'tomatoes','tomato','tomate','tomates','tomatillo', ...}
    """
    if not raw_label:
        return set()

    label = raw_label.strip().lower()
    # normalize hyphens/underscores
    label = label.replace('_', ' ').replace('-', ' ')

    candidates: Set[str] = set()
    candidates.add(label)

    # strip accents
    no_acc = _strip_accents(label)
    candidates.add(no_acc)

    # singularize simple english plurals
    singular = _singularize_en(no_acc)
    candidates.add(singular)

    # add translation (if known)
    # try singular english key, then raw
    if singular in EN_TO_ES:
        for t in EN_TO_ES[singular]:
            candidates.add(t)
            candidates.add(_strip_accents(t.lower()))
    if label in EN_TO_ES:
        for t in EN_TO_ES[label]:
            candidates.add(t)
            candidates.add(_strip_accents(t.lower()))

    # synonyms for english label
    if singular in SYNONYMS:
        for s in SYNONYMS[singular]:
            candidates.add(s)
            candidates.add(_strip_accents(s.lower()))
    if label in SYNONYMS:
        for s in SYNONYMS[label]:
            candidates.add(s)
            candidates.add(_strip_accents(s.lower()))

    # also try splitting multi-word labels and keep components
    parts = [p for p in label.split() if p]
    for p in parts:
        candidates.add(p)
        candidates.add(_strip_accents(p))
        candidates.add(_singularize_en(p))

    # final cleanup: strip and remove empty
    cleaned = {c.strip() for c in candidates if c and c.strip()}
    return cleaned


def map_label_to_db_candidates(raw_label: str) -> List[str]:
    """Convenience: devuelve lista ordenada de candidatos para consulta DB."""
    return sorted(list(generate_label_candidates(raw_label)))
