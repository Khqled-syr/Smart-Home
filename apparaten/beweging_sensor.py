from apparaten.apparaat import Apparaat


class Bewegingsensor(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.motion_detected = False

    def detect_motion(self, present=True):
        old_state = self.motion_detected
        self.motion_detected = present
        self.status = present

        if present and not old_state:
            return f"{self.name} gedetecteerde beweging"
        elif not present and old_state:
            return f"{self.name} geen beweging gedetecteerd"
        return None

    def get_status(self):
        return (
            "aan (beweging gedetecteerd)"
            if self.motion_detected
            else "uit (geen beweging gedetecteerd)"
        )
