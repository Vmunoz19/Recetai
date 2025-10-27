from django.views.decorators.http import require_POST
from django.http import JsonResponse
from PIL import Image
from apps.Core.services.vision.inference_pipeline import run_detection_and_freshness

@require_POST
def api_scan_ingredients(request):
    file = request.FILES.get("image")
    if not file:
        return JsonResponse({"error": "Falta la imagen"}, status=400)
    try:
        img = Image.open(file).convert("RGB")
        out = run_detection_and_freshness(img, do_freshness=True)
        return JsonResponse(out, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)