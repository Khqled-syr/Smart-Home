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

    if mode == "normaal":
        simulate_time = input("\nWilt u de dag/nacht cyclus simuleren? (ja/nee): ").lower()
        while simulate_time not in ["ja", "nee"]:
            simulate_time = input("Ongeldige invoer. Kies ja/nee: ").lower()
        simulate_time = simulate_time == "ja"
    else:
        simulate_time = False

    return mode, int(update_interval), simulate_time


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

    woonkamer.add_apparaat(Lamp("Woonkamer Lamp"))
    woonkamer.add_apparaat(Bewegingsensor("Woonkamer Bewegingsensor"))
    woonkamer.add_apparaat(Gordijn("Woonkamer Gordijn"))
    woonkamer.add_apparaat(Deurslot("Woonkamer Deurslot"))

    keuken.add_apparaat(Lamp("Keuken Lamp"))
    keuken.add_apparaat(Bewegingsensor("Keuken Bewegingsensor"))
    keuken.add_apparaat(RookSensor("Keuken Rookmelder"))
    keuken.add_apparaat(Thermostaat("Keuken Thermostaat"))

    slaapkamer.add_apparaat(Lamp("Slaapkamer Lamp"))
    slaapkamer.add_apparaat(Bewegingsensor("Slaapkamer Bewegingsensor"))
    slaapkamer.add_apparaat(Gordijn("Slaapkamer Gordijn"))

    badkamer.add_apparaat(Lamp("Badkamer Lamp"))
    badkamer.add_apparaat(Bewegingsensor("Badkamer Bewegingssensor"))

    gang.add_apparaat(Lamp("Gang Lamp"))
    gang.add_apparaat(Bewegingsensor("Gang Bewegingssensor"))
    gang.add_apparaat(Deurslot("Voordeur"))

    bewoner1 = Bewoner("Jan")
    bewoner2 = Bewoner("Marie")
    home.add_bewoner(bewoner1)
    home.add_bewoner(bewoner2)

    mode, update_interval, simulate_time = get_user_modus()
    if mode in ["nacht", "vakantie"]:
        simulate_time = False
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
