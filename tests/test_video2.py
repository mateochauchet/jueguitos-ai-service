import cv2
from app.utils.video_reader import read_video_frames
from app.detection.detector import BallDetector
from app.detection.humanDetector import HumanDetector
from app.tracking.tracker import ObjectTracker
from app.tracking.motion_analyzer import MotionAnalyzer
from pprint import pprint

video_path = "samples/test-jueguitos2.mp4"

if __name__ == "__main__":
    ball_detector = BallDetector()
    human_detector = HumanDetector()
    tracker = ObjectTracker()

    # Cargar todos los frames en memoria
    frames = list(read_video_frames(video_path))
    total_frames = len(frames)
    current_frame_idx = 0

    while True:
        frame = frames[current_frame_idx].copy()  # Copiar para no sobreescribir

        # Procesar detecciones
        ball_detections = ball_detector.detect_ball(frame)
        human_detections = human_detector.detect_human(frame)
        position = tracker.update(ball_detections)

        # Analizar velocidades solo si hay más de 1 posición
        velocity_info = None
        if len(tracker.positions) > 1:
            analyzer = MotionAnalyzer(tracker.positions)
            velocities = analyzer.compute_velocity()
            # Tomamos la velocidad del frame actual si existe
            if current_frame_idx > 0 and current_frame_idx - 1 < len(velocities):
                velocity_info = velocities[current_frame_idx - 1]["velocity"]

        # Ball data debug
        ball_data = {
            "label": ball_detections[0]["label"] if ball_detections else "No Ball",
            "confidence": round(ball_detections[0]["confidence"], 2) if ball_detections else None,
            "position": position,
            "velocity": round(velocity_info, 2) if velocity_info is not None else None
        }

        print("="*50)
        print(f"🎥 Frame {current_frame_idx + 1}/{total_frames}")
        print(f"⚽️ Ball Data:")
        pprint(ball_data)

        # Human data debug
        human_data = []
        for human in human_detections:
            human_data.append({
                "label": human["label"],
                "confidence": round(human["confidence"], 2),
                "position": human["box"]
            })
        if human_data:
            print(f"👨🏻‍🔧 Human Detections:")
            pprint(human_data)

        # Dibujar la pelota detectada
        for ball in ball_detections:
            x1, y1, x2, y2 = map(int, ball["box"])
            label = ball["label"]
            conf = ball["confidence"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Dibujar trayectoria de la pelota
        for i in range(1, len(tracker.positions)):
            pt1 = tuple(map(int, tracker.positions[i - 1]))
            pt2 = tuple(map(int, tracker.positions[i]))
            cv2.line(frame, pt1, pt2, (0, 0, 255), 2)

        # Dibujar humanos detectados
        for human in human_detections:
            x1, y1, x2, y2 = map(int, human["box"])
            label = human["label"]
            conf = human["confidence"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Dibujar máscara (si la tiene)
            if "mask" in human and human["mask"] is not None:
                mask = human["mask"].astype("uint8")
                color = (0, 255, 0)
                mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                colored_mask = cv2.merge([
                    mask_resized * color[0],
                    mask_resized * color[1],
                    mask_resized * color[2]
                ])
                frame = cv2.addWeighted(colored_mask, 0.5, frame, 1.0, 0)

        # Mostrar velocidad y frame actual en pantalla
        cv2.putText(frame, f"Frame: {current_frame_idx + 1}/{total_frames}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        if velocity_info is not None:
            cv2.putText(frame, f"Vel: {velocity_info:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        # Mostrar frame
        cv2.imshow("Tracking", frame)

        # Control manual
        key = cv2.waitKey(0)

        if key == ord('q'):
            break
        elif key == ord('d'):  # Siguiente
            if current_frame_idx < total_frames - 1:
                current_frame_idx += 1
        elif key == ord('a'):  # Anterior
            if current_frame_idx > 0:
                current_frame_idx -= 1
        elif key == ord('r'):  # Volver al primero
            current_frame_idx = 0

    cv2.destroyAllWindows()
