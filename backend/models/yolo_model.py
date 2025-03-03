from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Load YOLO model

def run_yolo(image):
    results = model(image)
    return results
