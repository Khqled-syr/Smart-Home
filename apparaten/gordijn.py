from apparaten.apparaat import Apparaat


class Gordijn(Apparaat):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.is_open = True
            return f"{self.name} geopend"
        return None

    def close(self):
        if self.is_open:
            self.is_open = False
            return f"{self.name} gesloten"
        return None

    def is_closed(self):
        return not self.is_open

    def get_status(self):
        return "open" if self.is_open else "dicht"

    def update_on_weather(self, zonnig: bool):
        if zonnig and self.is_open:
            return self.close()
        elif not zonnig and not self.is_open:
            return self.open()
        return None
