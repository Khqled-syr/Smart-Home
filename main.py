from apparaten.lamp import Lamp
from apparaten.rook_sensor import RookSensor
from apparaten.beweging_sensor import Bewegingsensor
from apparaten.thermostaat import Thermostaat
from apparaten.door_slot import Deurslot
from apparaten.gordijn import Gordijn
from woning.logger import Logger
from woning.bewoner import Bewoner
from woning.kamer import Kamer
from woning.smart_home import SmartHome
import time


def get_user_modus():
    print("\nWelkom bij de Smart Home Simulator!")

    mode = input("\nKies een modus (normaal/nacht/vakantie): ").lower()
    while mode not in ["normaal", "nacht", "vakantie"]:
        mode = input("Ongeldige modus. Kies normaal/nacht/vakantie: ").lower()

    update_interval = input("\nGeef de update interval in seconden (2-10): ")
    while not update_interval.isdigit() or not 2 <= int(update_interval) <= 10:
        update_interval = input("Ongeldige interval. Geef een waarde tussen 2-10: ")

    simulate_time = input("\nWilt u de dag/nacht cyclus simuleren? (ja/nee): ").lower()
    while simulate_time not in ["ja", "nee"]:
        simulate_time = input("Ongeldige invoer. Kies ja/nee: ").lower()

    return mode, int(update_interval), simulate_time == "ja"


if __name__ == "__main__":
    logger = Logger()
    home = SmartHome("Familie Slimme Woning", logger)

    woonkamer = Kamer("Woonkamer")
    keuken = Kamer("Keuken")
    slaapkamer = Kamer("Slaapkamer")
    badkamer = Kamer("Badkamer")
    gang = Kamer("Gang")

    for kamer in [woonkamer, keuken, slaapkamer, badkamer, gang]:
        home.add_kamer(kamer)

    woonkamer.add_device(Lamp("Woonkamer Lamp"))
    woonkamer.add_device(Bewegingsensor("Woonkamer Bewegingsensor"))
    woonkamer.add_device(Gordijn("Woonkamer Gordijn"))
    woonkamer.add_device(Deurslot("Woonkamer Deurslot"))

    keuken.add_device(Lamp("Keuken Lamp"))
    keuken.add_device(Bewegingsensor("Keuken Bewegingssensor"))
    keuken.add_device(RookSensor("Keuken Rookmelder"))
    keuken.add_device(Thermostaat("Keuken Thermostaat"))

    slaapkamer.add_device(Lamp("Slaapkamer Lamp"))
    slaapkamer.add_device(Bewegingsensor("Slaapkamer Bewegingssensor"))
    slaapkamer.add_device(Gordijn("Slaapkamer Gordijn"))

    badkamer.add_device(Lamp("Badkamer Lamp"))
    badkamer.add_device(Bewegingsensor("Badkamer Bewegingssensor"))

    gang.add_device(Lamp("Gang Lamp"))
    gang.add_device(Bewegingsensor("Gang Bewegingssensor"))
    gang.add_device(Deurslot("Voordeur"))

    bewoner1 = Bewoner("Jan")
    bewoner2 = Bewoner("Marie")
    home.add_bewoner(bewoner1)
    home.add_bewoner(bewoner2)

    mode, update_interval, simulate_time = get_user_modus()
    home.set_modus(mode)

    print("\nSmart Home Simulatie gestart...")
    try:
        while True:
            home.check_bewoner_beweging()
            if simulate_time:
                current_hour = time.localtime().tm_hour
                if 22 <= current_hour or current_hour < 6:
                    home.set_modus("nacht")
                else:
                    home.set_modus("normaal")
                    home.update_gordijnen(8 <= current_hour < 20)
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("\nSimulatie gestopt door gebruiker")
