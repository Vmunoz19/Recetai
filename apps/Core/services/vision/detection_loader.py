from functools import lru_cache
from ultralytics import YOLO
import os

@lru_cache(maxsize=1)
def get_detector():
    path = os.path.join("models", "vision", "detection", "food_yolov8.pt")
    if not os.path.exists(path):
        # fallback de prueba
        return YOLO("yolov8n.pt")
    return YOLO(path)