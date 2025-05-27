from woning.smart_hub import SmartHub
from woning.logger import Logger
from woning.bewoner import Bewoner
from woning.kamer import Kamer
from apparaten.lamp import Lamp
from apparaten.beweging_sensor import Bewegingsensor
from apparaten.rook_sensor import RookSensor
from apparaten.door_slot import Deurslot
from apparaten.gordijn import Gordijn
import random
import time
import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)
from _site.html_generator import HTMLGenerator


class SmartHome:
    def __init__(self, name: str, logger: Logger):
        self.name = name
        self.kamers = []
        self.residents = []
        self.logger = logger
        self.smart_hub = SmartHub(logger)
        self.mode = "normaal"
        self.gordijnen_status = {}
        self.smoke_timer = 0
        self.initialize_woning_regels()

    def add_kamer(self, kamer: Kamer):
        self.kamers.append(kamer)
        for apparaat in kamer.apparatten:
            if isinstance(apparaat, Gordijn):
                self.gordijnen_status[apparaat.name] = None

    def add_bewoner(self, bewoner: Bewoner):
        self.residents.append(bewoner)

    def set_modus(self, modus: str):
        if self.mode != modus:
            self.mode = modus.lower()
            self.logger.log(f"Woning in {modus}-modus gezet")
            self.initialize_modus()

    def initialize_modus(self):
        for kamer in self.kamers:
            for apparaat in kamer.apparatten:
                if isinstance(apparaat, Lamp):
                    if self.mode == "nacht":
                        apparaat.zet_uit()
                        apparaat.set_brightness(30)
                    elif self.mode == "vakantie":
                        apparaat.zet_uit()
                        apparaat.set_brightness(50)
                elif isinstance(apparaat, Gordijn):
                    if self.mode == "vakantie":
                        apparaat.close()

        self.refresh_deurs()

    def refresh_deurs(self):
        for kamer in self.kamers:
            for apparaat in kamer.apparatten:
                if isinstance(apparaat, Deurslot):
                    if self.mode in ["nacht", "vakantie"]:
                        apparaat.lock_door()
                    else:
                        if kamer.check_bewoners():
                            apparaat.open_door()
                        else:
                            if apparaat.name != "Voordeur":
                                apparaat.lock_door()

    def initialize_woning_regels(self):
        def motion_licht_regel(home):
            for kamer in home.kamers:
                if kamer.check_bewoners():
                    motion_sensors = [
                        d for d in kamer.apparatten if isinstance(d, Bewegingsensor)
                    ]
                    lamps = [d for d in kamer.apparatten if isinstance(d, Lamp)]
                    if motion_sensors and lamps and home.mode != "nacht":
                        return True, kamer, lamps
            return False, None, None

        def activeer_lichten(home):
            _, kamer, lamps = motion_licht_regel(home)
            if kamer and lamps:
                lampen_aan = False
                for lamp in lamps:
                    if not lamp.status:
                        lamp.zet_aan()
                        lampen_aan = True
                if lampen_aan:
                    return f"Lampen aangezet in {kamer.name}"
            return None

        def check_kamer_status(home):
            kamers_uitgezet = []
            for kamer in home.kamers:
                if not kamer.check_bewoners():
                    for apparaat in kamer.apparatten:
                        if isinstance(apparaat, Lamp):
                            apparaat.zet_uit()
                        elif isinstance(apparaat, Bewegingsensor):
                            apparaat.detect_motion(False)
                    kamers_uitgezet.append(kamer.name)

                if kamer.name == "Keuken":
                    home.smoke_timer += 1
                    if home.smoke_timer >= 5:
                        home.smoke_timer = 0
                        for apparaat in kamer.apparatten:
                            if isinstance(apparaat, RookSensor):
                                if kamer.check_bewoners():
                                    if random.random() < 0.1:
                                        return f"ALARM: {apparaat.detect_smoke(True)} in Keuken!"
                                elif apparaat.smoke_detected:
                                    apparaat.detect_smoke(False)
                                    return "Rook verdwenen in Keuken"

            if kamers_uitgezet:
                return f"Apparaten uit in: {', '.join(kamers_uitgezet)}"
            return None

        self.smart_hub.add_rule(lambda h: motion_licht_regel(h)[0], activeer_lichten)
        self.smart_hub.add_rule(lambda h: True, check_kamer_status)

    def check_bewoner_beweging(self):
        events = []
        current_hour = time.localtime().tm_hour
        self.refresh_deurs()

        for kamer in self.kamers:
            for apparaat in kamer.apparatten:
                if isinstance(apparaat, Lamp):
                    if self.mode == "nacht":
                        apparaat.set_brightness(30)
                    elif self.mode == "vakantie":
                        apparaat.set_brightness(50)
                    elif not kamer.check_bewoners():
                        apparaat.set_brightness(20)
                    elif current_hour >= 18 or current_hour < 6:
                        apparaat.set_brightness(60)
                    else:
                        apparaat.set_brightness(100)

            if not kamer.check_bewoners():
                for apparaat in kamer.apparatten:
                    if isinstance(apparaat, Bewegingsensor):
                        apparaat.detect_motion(False)

        for resident in self.residents:
            if random.random() < 0.3:
                target_room = random.choice(self.kamers)
                if resident.current_room != target_room:
                    move_message = resident.move_to(target_room)
                    if move_message:
                        self.logger.log(move_message)
                        events.append(("movement", resident, target_room))

                        for apparaat in target_room.apparatten:
                            if isinstance(apparaat, Bewegingsensor):
                                sensor_message = apparaat.detect_motion(True)
                                if sensor_message:
                                    self.logger.log(sensor_message)
                                    events.append(
                                        ("motion_detected", apparaat, target_room)
                                    )

        self.refresh_deurs()
        self.smart_hub.process_events(self)

        for event_type, source, target in events:
            if event_type == "movement" and isinstance(target, Kamer):
                for apparaat in target.apparatten:
                    if isinstance(apparaat, Lamp) and not apparaat.status:
                        message = apparaat.zet_aan()
                        if message:
                            self.logger.log(message)

        HTMLGenerator.generate_home_status(self)

    def update_gordijnen(self, zonnig: bool):
        for kamer in self.kamers:
            for apparaat in kamer.apparatten:
                if isinstance(apparaat, Gordijn):
                    current_status = "dicht" if apparaat.is_closed() else "open"
                    if self.gordijnen_status.get(apparaat.name) != current_status:
                        apparaat.update_on_weather(zonnig)
                        new_status = "dicht" if apparaat.is_closed() else "open"
                        if current_status != new_status:
                            self.logger.log(f"Gordijn in {kamer.name}: {new_status}")
                            self.gordijnen_status[apparaat.name] = new_status
