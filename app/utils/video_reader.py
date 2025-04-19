import cv2

def read_video_frames(video_path: str):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"No se pudo abrir el video: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()
