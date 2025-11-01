from functools import lru_cache
from ultralytics import YOLO
import os
from django.conf import settings

@lru_cache(maxsize=1)
def get_detector():
    """
    Carga el detector YOLO. Intenta pesos específicos de comida; si no existen,
    cae a yolov8n.pt (COCO) y avisa por consola.
    """
    base = getattr(settings, "BASE_DIR", ".")
    specific = os.path.join(base, "models", "vision", "detection", "food_yolov8.pt")
    if os.path.exists(specific):
        print(f"[vision] Using detector: {specific}")
        return YOLO(specific)

    print("[vision] food_yolov8.pt not found; using fallback yolov8n.pt (COCO).")
    return YOLO("yolov8n.pt")