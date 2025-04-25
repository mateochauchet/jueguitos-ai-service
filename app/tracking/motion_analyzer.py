import math

class MotionAnalyzer:
    def __init__(self, positions, fps=None):
        self.positions = positions
        self.fps = fps  # Si lo querés usar para velocidad real (opcional)

    def compute_velocity(self):
        velocities = []
        for i in range(1, len(self.positions)):
            x1, y1 = self.positions[i - 1]
            x2, y2 = self.positions[i]
            dx = x2 - x1
            dy = y2 - y1
            velocity = math.sqrt(dx ** 2 + dy ** 2)
            velocities.append({"frame": i, "velocity": velocity})
        return velocities

    def compute_acceleration(self, velocities=None):
        if velocities is None:
            velocities = self.compute_velocity()
        accelerations = []
        for i in range(1, len(velocities)):
            dv = velocities[i]["velocity"] - velocities[i - 1]["velocity"]
            accelerations.append({"frame": velocities[i]["frame"], "acceleration": dv})
        return accelerations

    def compute_total_distance(self):
        distance = 0
        for i in range(1, len(self.positions)):
            x1, y1 = self.positions[i - 1]
            x2, y2 = self.positions[i]
            distance += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance
