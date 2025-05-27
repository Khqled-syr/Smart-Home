from apparaten.apparaat import Apparaat


class RookSensor(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.smoke_detected = False
        self.alarm_active = False

    def detect_smoke(self, detected=True):
        self.smoke_detected = detected
        if detected:
            self.activate_alarm()
        return (
            f"{self.name} Rook decteert"
            if detected
            else f"{self.name} geen rook gedecteerd"
        )

    def activate_alarm(self):
        self.alarm_active = True
        return f"{self.name} alarm geactiveerd"

    def deactivate_alarm(self):
        self.alarm_active = False
        return f"{self.name} alarm deactiveerd"

    def get_status(self):
        return "Rook gedetecteerd" if self.smoke_detected else "Geen rook gedecteerd"
