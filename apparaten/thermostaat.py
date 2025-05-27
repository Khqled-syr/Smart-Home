from apparaten.apparaat import Apparaat


class Thermostaat(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.temperature = 21

    def set_temperature(self, temp: float):
        self.temperature = temp
        return f"{self.name} tempratuur verplaatst naar {temp}C"
