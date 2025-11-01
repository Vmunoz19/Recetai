from ultralytics import YOLO

# Carga el mismo modelo que usa tu proyecto
model = YOLO("models/vision/detection/food_yolov8.pt")  # o "yolov8n.pt" si no tienes el otro

# Imprime todas las clases disponibles
print("Total clases:", len(model.names))
for i, name in model.names.items():
    print(f"{i:02d} - {name}")