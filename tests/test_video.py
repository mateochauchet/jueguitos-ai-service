# import sys
# sys.path.append(".")
# from app.utils.video_reader import read_video_frames
# import cv2

video_path = "samples/test-jueguitos.mp4"

# if __name__ == "__main__":
#     for i, frame in enumerate(read_video_frames(video_path)):
#         cv2.imshow("Frame", frame)

#         # Sale con 'q'
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()

# from app.utils.video_reader import read_video_frames
# from app.detection.detector import BallDetector
# import cv2

# if __name__ == "__main__":
#     detector = BallDetector()

#     for frame in read_video_frames(video_path):
#         detections = detector.detect_ball(frame)

#         for det in detections:
#             x1, y1, x2, y2 = map(int, det["box"])
#             label = det["label"]
#             conf = det["confidence"]
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


#         cv2.imshow("Detections", frame)

#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()


from app.utils.video_reader import read_video_frames
from app.detection.detector import BallDetector
from app.tracking.tracker import ObjectTracker
import cv2

if __name__ == "__main__":
    detector = BallDetector()
    tracker = ObjectTracker()

    for frame in read_video_frames(video_path):
        detections = detector.detect_ball(frame)
        position = tracker.update(detections)

        # Dibujar la pelota detectada
        for det in detections:
            x1, y1, x2, y2 = map(int, det["box"])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Dibujar trayectoria
        for i in range(1, len(tracker.positions)):
            pt1 = tuple(map(int, tracker.positions[i - 1]))
            pt2 = tuple(map(int, tracker.positions[i]))
            cv2.line(frame, pt1, pt2, (0, 0, 255), 2)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


