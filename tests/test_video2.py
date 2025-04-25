# import sys
# sys.path.append(".")
# from app.utils.video_reader import read_video_frames
# import cv2

video_path = "samples/test-jueguitos2.mp4"

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
#from app.detection.humanBoxDetector import HumanBoxDetector
from app.detection.humanDetector import HumanDetector
from app.tracking.tracker import ObjectTracker
from app.counting.counter import Counter
#from app.counting.counter import is_mask_inside_box
import cv2

if __name__ == "__main__":
    ball_detector = BallDetector()
    human_detector = HumanDetector()
    human_detector = HumanDetector()

    tracker = ObjectTracker()
    counter = Counter()

    for frame in read_video_frames(video_path):
        ball_detections = ball_detector.detect_ball(frame)
        human_detections = human_detector.detect_human(frame)
        human_detections = human_detector.detect_human(frame)
        position = tracker.update(ball_detections)

         # Actualizamos el contador de jueguitos
        count = counter.update(position, ball_detections, human_detections, frame)

        # Dibujar la pelota detectada
        for ball in ball_detections:
            x1, y1, x2, y2 = map(int, ball["box"])
            label = ball["label"]
            conf = ball["confidence"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(frame, f"Jueguitos: {count[0]}, {count[1]}, {count[2]}, {count[3]}", (x1, y2 + 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Dibujar trayectoria
        for i in range(1, len(tracker.positions)):
            pt1 = tuple(map(int, tracker.positions[i - 1]))
            pt2 = tuple(map(int, tracker.positions[i]))
            cv2.line(frame, pt1, pt2, (0, 0, 255), 2)
        # Dibujar mask de humanos detectado
        for human in human_detections:
            x1, y1, x2, y2 = map(int, human["box"])
            label = human["label"]
            conf = human["confidence"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            mask = human["mask"].astype("uint8")
            if counter.is_mask_inside_box(ball["box"], mask, frame):
                cv2.putText(frame, "DENTROOOOO", (int(ball["box"][0]), int(ball["box"][3]) + 22),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


            color = (0, 255, 0)
            mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            colored_mask = cv2.merge([
                mask_resized * color[0],
                mask_resized * color[1],
                mask_resized * color[2]
            ])

            frame = cv2.addWeighted(colored_mask, 0.5, frame, 1.0, 0)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


