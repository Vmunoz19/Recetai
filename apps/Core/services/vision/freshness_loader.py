"""
Evaluador heurístico de frescura (versión sin modelo entrenado).
Analiza el color promedio del recorte de imagen y estima un nivel de frescura.
"""

import numpy as np
from PIL import Image
import colorsys
import random

def _analyze_color(pil_img: Image.Image):
    img = pil_img.convert("RGB").resize((64, 64))
    np_img = np.array(img) / 255.0
    r_avg, g_avg, b_avg = np.mean(np_img, axis=(0, 1))
    h, s, v = colorsys.rgb_to_hsv(r_avg, g_avg, b_avg)
    return h, s, v

def _decide_freshness(h, s, v):
    if v > 0.55 and s > 0.35:
        return "fresh", round(random.uniform(0.80, 0.95), 2)
    elif (0.40 <= v <= 0.55) or (0.20 <= s <= 0.35):
        return "medium", round(random.uniform(0.60, 0.75), 2)
    else:
        return "rotten", round(random.uniform(0.40, 0.59), 2)

def classify_fruit_freshness(pil_img: Image.Image) -> dict:
    h, s, v = _analyze_color(pil_img)
    label, conf = _decide_freshness(h, s, v)
    print(f"[vision:freshness:heuristic] s={s:.2f}, v={v:.2f} → {label.upper()} ({conf})")
    return {
        "raw_label": "heuristic_freshness",
        "simple": label,
        "confidence": conf
    }

get_fruit_classifier = lambda: None
