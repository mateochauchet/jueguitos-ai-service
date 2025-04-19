import math

class ObjectTracker:
    def __init__(self):
        self.positions = []  # Lista de posiciones (centros) del objeto

    def update(self, detections):
        """
        Recibe detecciones de objetos en un frame, y actualiza el tracking.
        Solo usamos la primera detección por ahora (una sola pelota).
        """
        if not detections:
            return None  # No se detectó pelota en este frame

        # Tomamos el primer bounding box
        box = detections[0]["box"]
        x1, y1, x2, y2 = box
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        position = (cx, cy)

        # Guardamos la posición
        self.positions.append(position)

        return position

    def get_last_position(self):
        if self.positions:
            return self.positions[-1]
        return None

    def get_trajectory(self):
        return self.positions
