from apparaten.apparaat import Apparaat
from apparaten.beweging_sensor import Bewegingsensor


class Kamer:
    def __init__(self, name: str):
        self.name = name
        self.apparatten = []
        self.bewoners = []

    def add_device(self, apparaat: Apparaat):
        self.apparatten.append(apparaat)

    def add_bewoner(self, resident):
        self.bewoners.append(resident)
        for apparaat in self.apparatten:
            if isinstance(apparaat, Bewegingsensor):
                apparaat.detect_motion(True)

    def remove_bewoner(self, resident):
        if resident in self.bewoners:
            self.bewoners.remove(resident)
            if not self.bewoners:
                for apparaat in self.apparatten:
                    if isinstance(apparaat, Bewegingsensor):
                        apparaat.detect_motion(False)

    def check_bewoners(self):
        return len(self.bewoners) > 0
