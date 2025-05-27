from apparaten.apparaat import Apparaat


class Deurslot(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.locked = True

    def lock_door(self):
        self.locked = True
        return f"{self.name} gesloten"

    def open_door(self):
        self.locked = False
        return f"{self.name} open"

    def get_status(self):
        return "gesloten" if self.locked else "open"
