from functools import lru_cache
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os

# Mapea índices → etiquetas
FRUIT_FRESHNESS_LABELS = [
    "freshapples","freshbanana","freshmango","freshoranges","freshtomato",
    "rottenapples","rottenbanana","rottenmango","rottenoranges","rottentomato"
]

# Si prefieres binario por fruta, puedes colapsar a fresh/rotten por prefijo.
def label_to_simple(tag: str) -> str:
    return "fresh" if tag.startswith("fresh") else "rotten"

@lru_cache(maxsize=1)
def get_fruit_classifier():
    path = os.path.join("models","vision","freshness","fruit_effb0.pth")
    model = torch.load(path, map_location="cpu")  # el repo trae el .pth listo
    model.eval()
    return model

# Transform estándar (ajústala si el repo define otra)
FRUIT_TFMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def classify_fruit_freshness(pil_img: Image.Image) -> dict:
    model = get_fruit_classifier()
    with torch.no_grad():
        x = FRUIT_TFMS(pil_img).unsqueeze(0)
        logits = model(x)
        if isinstance(logits, (list, tuple)):
            logits = logits[0]
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        idx = int(probs.argmax())
        raw_label = FRUIT_FRESHNESS_LABELS[idx]
        return {
            "raw_label": raw_label,
            "simple": label_to_simple(raw_label),
            "confidence": float(probs[idx])
        }