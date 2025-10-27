import numpy as np
from PIL import Image
from .detection_loader import get_detector
from .freshness_loader import classify_fruit_freshness

# Si quieres aplicar frescura solo a frutas conocidas
FRUIT_NAMES = {"apple","banana","orange","mango","tomato","strawberry","pear","grape","peach","plum","pineapple","kiwi","watermelon","papaya","lemon","lime"}

def run_detection_and_freshness(pil_image: Image.Image, do_freshness=True):
    det_model = get_detector()
    # YOLO acepta PIL directamente
    results = det_model.predict(pil_image, verbose=False)

    detections = []
    if len(results):
        r = results[0]
        boxes = r.boxes.xyxy.cpu().numpy()     # (N,4)
        scores = r.boxes.conf.cpu().numpy()    # (N,)
        classes = r.boxes.cls.cpu().numpy()    # (N,)
        names = r.names                         # dict idx->name

        for i, (x1, y1, x2, y2) in enumerate(boxes):
            label = names[int(classes[i])].lower()
            score = float(scores[i])
            item = {
                "label": label,
                "score": score,
                "box": [float(x1), float(y1), float(x2), float(y2)]
            }

            # Clasificación de frescura solo si es fruta y el flag lo pide
            if do_freshness and any(k in label for k in FRUIT_NAMES):
                crop = pil_image.crop((x1, y1, x2, y2))
                try:
                    fres = classify_fruit_freshness(crop)
                    item["freshness"] = fres["simple"]
                    item["freshness_conf"] = fres["confidence"]
                except Exception:
                    item["freshness"] = None
                    item["freshness_conf"] = None

            detections.append(item)

    # Resumen para búsqueda en BD (no guardes nada; solo mapea nombres si quieres)
    detected_names = sorted(list({d["label"] for d in detections}))
    return {"detected": detections, "detected_summary": detected_names, "count": len(detections)}