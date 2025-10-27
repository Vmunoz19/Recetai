MAPEO = {
    "apple": "Manzana",
    "banana": "Plátano",
    "broccoli": "Brócoli",
    "tomato": "Tomate",
    # ...
}

def to_db_name(model_label: str) -> str | None:
    return MAPEO.get(model_label.lower())