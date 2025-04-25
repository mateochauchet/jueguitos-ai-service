import numpy as np
import cv2

class Counter:
    def __init__(self):
        self.last_y = None
        self.last_x = None
        self.direction_y = None
        self.direction_x = None
        #self.count = 0
        self.count = [0,0,0,0]
    def update(self, position, ball_detections, human_detections, frame):
        if not ball_detections or not human_detections:
            return self.count

        ball_box = ball_detections[0]["box"]
        human_box = human_detections[0]["box"]
        mask = human_detections[0]["mask"].astype("uint8")
        
        if self.ball_under_human(ball_box, human_box):
            self.count[2] += 1
            return self.count
        if not self.is_mask_inside_box(ball_box, mask, frame):
            self.count[3] += 1
            return self.count
        x, y = position

        if self.direction_y_change(y):
            self.count[0] += 1
        elif self.direction_x_change(x):
            self.count[1] += 1
        
        return self.count

    def get_count(self):
        return self.count
    
    def ball_under_human(self, ball_box, human_box):    #Lógica: Si punto más bajo de Pelota menor que punto más bajo que Humano no sumar toque.
        ball_y2 = ball_box[3]
        human_y2 = human_box[3]
        return ball_y2 > human_y2

    def is_mask_inside_box(self, ball_box, mask, frame, threshold_pixels=5):    #Lógica: Si Box de Pelota no toca a Mask Humano no sumar toque.
        x1, y1, x2, y2 = map(int, ball_box)
        mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        
        mask_region = mask_resized[y1:y2, x1:x2]
        
        person_pixels_inside = np.sum(mask_region)  # Cantidad de píxeles de Persona en la región

        return person_pixels_inside >= threshold_pixels
    
    def direction_y_change(self, position_y):   #Lógica: Suma cuando la pelota cambia de dirección vertical (baja y luego sube).
        change = False
        if self.last_y is not None:
            delta_y = position_y - self.last_y

            new_direction_y = 1 if delta_y > 0 else -1  # Dirección actual (arriba: -1, abajo: 1)

            # Cambio de dirección (de bajada a subida → contacto con el pie)
            if self.direction_y == 1 and new_direction_y == -1:
                change = True
            self.direction_y = new_direction_y
        self.last_y = position_y
        return change

    def direction_x_change(self, position_x):   #Lógica: Suma cuando la pelota cambia de dirección vertical.
        change = False
        min_delta = 5  # Umbral para ignorar movimientos menores (ajustable)
        
        if self.last_x is not None:
            delta_x = position_x - self.last_x
            if abs(delta_x) > min_delta:
                new_direction_x = 1 if delta_x > 0 else -1

                if self.direction_x is not None and new_direction_x != self.direction_x:
                    change = True

                self.direction_x = new_direction_x

        self.last_x = position_x
        return change