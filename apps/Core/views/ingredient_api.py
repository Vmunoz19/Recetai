from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io

from apps.Core.services.vision.inference_pipeline import run_detection_and_freshness
from apps.Core.services.vision.label_mapper import map_label_to_db_candidates
from apps.Core.models import Ingrediente, Receta
from apps.Core.services.vision.detection_loader import get_detector
import time, os


@csrf_exempt
@require_POST
def detect_ingredients_api(request):
    """
    Endpoint que recibe una imagen (multipart form, campo 'image') y
    devuelve JSON con las detecciones y recetas coincidentes mapeadas
    contra la BD. No modifica la BD.
    """
    # Log minimal info for debugging in dev
    # (avoid sensitive logging in production)
    # print('detect_ingredients_api called, files:', list(request.FILES.keys()))

    img_file = request.FILES.get('image')
    if not img_file:
        return JsonResponse({'error': 'No image provided'}, status=400)

    try:
        img = Image.open(img_file).convert('RGB')
    except Exception as e:
        return JsonResponse({'error': 'Invalid image', 'details': str(e)}, status=400)

    # DEBUG: save received image so developer can inspect the exact frame
    try:
        debug_dir = os.path.join('runs', 'debug_uploads')
        os.makedirs(debug_dir, exist_ok=True)
        fname = f"capture_{int(time.time())}.jpg"
        save_path = os.path.join(debug_dir, fname)
        img.save(save_path, format='JPEG')
        print('detect_ingredients_api: saved uploaded image to', save_path)
    except Exception as e:
        print('detect_ingredients_api: failed saving upload', str(e))

    # Ejecutar detección y frescura (interno, puede tardar)
    try:
        out = run_detection_and_freshness(img, do_freshness=True)
    except Exception as e:
        print('detect_ingredients_api: detection error', str(e))
        return JsonResponse({'error': 'Detection failed', 'details': str(e)}, status=500)

    detected = out.get('detected', [])
    detected_names = [d['label'] for d in detected]
    # debug: print minimal summary to console for dev
    try:
        print('detect_ingredients_api: received image, detections:', len(detected), 'summary:', detected_names)
    except Exception:
        pass

    # DEBUG: run the underlying YOLO predict here as well and print raw info (boxes, classes, scores)
    try:
        det_model = get_detector()
        results = det_model.predict(img, verbose=False)
        if len(results):
            r = results[0]
            try:
                boxes = r.boxes.xyxy.cpu().numpy()
                scores = r.boxes.conf.cpu().numpy()
                classes = r.boxes.cls.cpu().numpy()
                names = r.names
                print('detect_ingredients_api: yolo raw -> boxes:', boxes.shape[0], 'names_keys:', list(names.values())[:10])
                # print classes and highest scores for quick inspection
                if boxes.shape[0] > 0:
                    for i in range(min(10, boxes.shape[0])):
                        cls = int(classes[i])
                        print(f' - box {i}: class={cls} name={names.get(cls)} score={float(scores[i])}')
            except Exception as e:
                print('detect_ingredients_api: error reading result boxes', str(e))
        else:
            print('detect_ingredients_api: yolo predict returned 0 results')
    except Exception as e:
        print('detect_ingredients_api: error running direct yolo predict', str(e))

    # Mapear nombres detectados contra Ingrediente.nombre_singular
    matched_ingredientes = {}
    for name in detected_names:
        # generar candidatos (inglés->es, sinónimos, normalización)
        candidates = map_label_to_db_candidates(name)
        found = set()
        for c in candidates:
            qs = Ingrediente.objects.filter(nombre_singular__icontains=c)
            for v in qs.values_list('nombre_singular', flat=True):
                found.add(v)
        matched_ingredientes[name] = sorted(list(found))

    # Buscar recetas que contengan al menos uno de los ingredientes mapeados
    # Recolectar todos nombres posibles para consulta
    possible_names = set()
    for vals in matched_ingredientes.values():
        for v in vals:
            possible_names.add(v)

    matching_recipes = []
    if possible_names:
        # Buscar recetas con ingredientes cuyo nombre coincida con alguno de los posibles
        recs = Receta.objects.prefetch_related('ingredientes').all()
        for r in recs:
            receta_ing_names = [i.nombre_singular.lower() for i in r.ingredientes.all()]
            matched = [n for n in receta_ing_names if any(p.lower() in n for p in possible_names)]
            if matched:
                total = max(1, len(receta_ing_names))
                match_pct = round((len(matched) / total) * 100, 1)
                matching_recipes.append({
                    'id': r.id,
                    'nombre': r.nombre,
                    'image_url': r.image_url,
                    'matched_ingredients': matched,
                    'matched_count': len(matched),
                    'total_ingredients': total,
                    'match_percentage': match_pct,
                })

        # Ordenar por porcentaje desc
        matching_recipes = sorted(matching_recipes, key=lambda x: x['match_percentage'], reverse=True)[:50]

    resp = {
        'detected': detected,
        'detected_summary': detected_names,
        'mapped_ingredients': matched_ingredientes,
        'matching_recipes': matching_recipes,
    }
    return JsonResponse(resp)
