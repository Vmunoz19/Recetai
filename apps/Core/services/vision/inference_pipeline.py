import numpy as np
from PIL import Image
from .detection_loader import get_detector
from .freshness_loader import classify_fruit_freshness

# Conjunto de frutas conocidas para aplicar frescura
FRUIT_NAMES = {
    "apple","banana","orange","mango","tomato","strawberry",
    "plum","pineapple","kiwi","watermelon","papaya","lemon","lime",
    "pear","peach","grape","raspberry","blueberry","guava","cherry",
    "coconut","passion fruit"
}

def _is_fruit_label(label: str) -> bool:
    if not label:
        return False
    lbl = label.strip().lower()
    return lbl in FRUIT_NAMES

def run_detection_and_freshness(pil_image: Image.Image, do_freshness: bool = True):
    """
    Ejecuta detección YOLO y, opcionalmente, clasifica frescura para frutas.
    Devuelve:
      {
        "detected": [{x1,y1,x2,y2,score,label, freshness?, freshness_conf?}, ...],
        "detected_summary": [labels únicos ordenados],
        "count": n
      }
    """
    det_model = get_detector()
    # YOLO (ultralytics) acepta PIL directamente
    results = det_model.predict(pil_image, verbose=False)

    detections = []
    if len(results):
        r = results[0]
        if hasattr(r, "boxes") and r.boxes is not None:
            for b in r.boxes:
                xyxy = b.xyxy[0].cpu().numpy().tolist()
                x1, y1, x2, y2 = [int(v) for v in xyxy]
                score = float(b.conf[0].cpu().numpy()) if hasattr(b, "conf") else None
                # Nombre de clase
                cls_idx = int(b.cls[0].cpu().numpy()) if hasattr(b, "cls") else None
                label = str(r.names.get(cls_idx, cls_idx)) if hasattr(r, "names") else str(cls_idx)

                item = {
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "score": score, "label": label,
                }

                # Clasificación de frescura sólo para frutas conocidas
                if do_freshness and _is_fruit_label(label):
                    crop = pil_image.crop((x1, y1, x2, y2))
                    try:
                        fres = classify_fruit_freshness(crop)
                        item["freshness"] = fres["simple"]
                        item["freshness_conf"] = fres["confidence"]
                    except Exception:
                        # No romper el flujo si faltan pesos de frescura
                        item["freshness"] = None
                        item["freshness_conf"] = None

                detections.append(item)
    

    detected_names = sorted(list({d["label"] for d in detections}))
    if detections:
        print("\n[vision] === DETECCIONES DEL MODELO ===")
        for i, d in enumerate(detections, 1):
            label = d.get("label")
            score = d.get("score")
            fresh = d.get("freshness")
            conf_fresh = d.get("freshness_conf")
            print(f" {i:02d}. {label:<15} score={score:.2f}", end="")
            if fresh:
                print(f" | frescura={fresh} ({conf_fresh:.2f})")
            else:
                print()
        print(f"[vision] Total detectados: {len(detections)}\n")
    else:
        print("[vision] No se detectó ningún objeto.")
    return {
        "detected": detections,
        "detected_summary": detected_names,
        "count": len(detections)
    }
