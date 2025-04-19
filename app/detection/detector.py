from ultralytics import YOLO
import cv2

class BallDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect_ball(self, frame):
        results = self.model(frame)[0]
        detections = []

        for result in results.boxes:
            class_id = int(result.cls[0])
            conf = float(result.conf[0])
            box = result.xyxy[0].tolist()  # [x1, y1, x2, y2]

            # El ID 32 en COCO es pelota de fútbol
            if class_id == 32 and conf > 0.5:
                detections.append({
                    "box": box,
                    "confidence": conf,
                    "class_id": class_id
                })

        return detections
