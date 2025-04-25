from ultralytics import YOLO
import cv2

class HumanDetector:
    def __init__(self, model_path="yolov8n-seg.pt"):
        self.model = YOLO(model_path)

    def detect_human(self, frame):
        results = self.model(frame)[0]
        
        if results.masks is not None:
            masks = results.masks.data  # tensor: [N, H, W]
        
        detections = []

        for i, result in enumerate(results.boxes):
            class_id = int(result.cls[0])
            conf = float(result.conf[0])
            label = self.model.names[class_id]
            box = result.xyxy[0].tolist()  # [x1, y1, x2, y2]

            # El ID 0 en COCO es persona
            if class_id == 0 and conf > 0.5:
                detections.append({
                    "box": box,
                    "label": label,
                    "confidence": conf,
                    "class_id": class_id,
                    "mask": results.masks.data[i].cpu().numpy()
                })
        return detections

