class Apparaat:
    def __init__(self, name: str):
        self.name = name
        self.status = False

    def zet_aan(self):
        self.status = True
        return f"{self.name} aangeschakeld"

    def zet_uit(self):
        self.status = False
        return f"{self.name} uitgeschakeld"

    def get_status(self):
        return "aan" if self.status else "uit"
