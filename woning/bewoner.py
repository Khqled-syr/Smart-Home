from woning.kamer import Kamer


class Bewoner:
    def __init__(self, name: str):
        self.name = name
        self.current_room = None

    def move_to(self, new_room):
        if self.current_room:
            self.current_room.remove_bewoner(self)
        new_room.add_bewoner(self)
        self.current_room = new_room
        return f"{self.name} is nu in de kamer: {new_room.name}"
