from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io

from django.db.models import Count, F, Q
from apps.Core.services.vision.inference_pipeline import run_detection_and_freshness
from apps.Core.services.vision.label_mapper import map_label_to_db_candidates, buscar_en_bd
from apps.Core.models import Ingrediente, Receta

@csrf_exempt
@require_POST
def detect_ingredients_api(request):
    """
    Espera FormData con 'image' (blob).
    Devuelve ingredientes detectados con nivel de frescura (🟢🟡🔴).
    """
    if 'image' not in request.FILES:
        return JsonResponse({"error": "image file missing"}, status=400)

    img_bytes = request.FILES['image'].read()
    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # 1️⃣ Detección principal
    result = run_detection_and_freshness(pil_img, do_freshness=True)
    detections = result.get("detected", [])
    detected_names = result.get("detected_summary", [])

    # 2️⃣ Mapeo a ingredientes BD
    matched_ingredientes = []
    final_ingredients = []

    for det in detections:
        label = det.get("label", "")
        score = det.get("score", 0)
        freshness = det.get("freshness", None)

        candidates = map_label_to_db_candidates(label)
        qs = buscar_en_bd(candidates)
        items = list(qs.values("id", "nombre_singular"))

        if not items:
            continue

        # Tomamos el primer match válido
        ing_name = items[0]["nombre_singular"]
        conf_match = round(score, 2)
        freshness_state = freshness or "medium"

        # Asignar color de semáforo
        if freshness_state == "fresh":
            emoji = "🟢"
        elif freshness_state == "medium":
            emoji = "🟡"
        else:
            emoji = "🔴"

        matched_ingredientes.append({
            "label": label,
            "ingrediente": ing_name,
            "match": conf_match,
            "freshness": freshness_state,
            "emoji": emoji,
        })

        # lista compacta para front
        final_ingredients.append([ing_name, conf_match, freshness_state])

    resp = {
        "ingredients": final_ingredients,
        "mapped_ingredients": matched_ingredientes,
        "detected_summary": detected_names,
    }
    return JsonResponse(resp)
