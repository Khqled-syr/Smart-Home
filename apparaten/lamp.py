from apparaten.apparaat import Apparaat


class Lamp(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.brightness = 50

    def set_brightness(self, level: int):
        if 0 <= level <= 100:
            self.brightness = level
            return f"{self.name} brightness ingesteld op {level}%"
        return f"Ongeldige brightness voor {self.name}"

    def get_status(self):
        return (
            f"aan (brightness: {self.brightness}%)"
            if self.status
            else f"uit (brightness: {self.brightness}%)"
        )
