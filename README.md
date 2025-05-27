# Slim Huis Simulator

## Wat doet dit project?
Dit is een simulator voor een slim huis dat ik heb gemaakt voor mijn Python cursus. Het huis heeft:
- Slimme lampen die automatisch aan/uit gaan
- Deuren die automatisch op slot gaan 's nachts
- Bewegingssensoren die zien waar mensen zijn
- Rookmelders voor veiligheid
- Een systeem dat alles slim aanstuurt

## Hoe werkt het?
Het huis kan in verschillende standen werken:
- **Normaal**: Overdag, als mensen thuis zijn
- **Nacht**: 's Avonds, lampen dimmen en deuren op slot
- **Vakantie**: Als niemand thuis is, extra beveiliging

## Hoe start je het op?
1. Download de code
2. Open een terminal in de project map
3. Start het programma:
```powershell
python main.py
```

## Wat kun je instellen?
Als je het programma start, kun je kiezen:
- Welke modus je wilt (normaal/nacht/vakantie)
- Hoe snel het systeem moet updaten (2-10 seconden)
- Of je de dag/nacht cyclus wilt simuleren

## Project Structuur
```
Project/
├── main.py              # Start het programma
├── apparaten/           # Alle slimme apparaten
│   ├── lamp.py         # Slimme lampen
│   ├── door_slot.py    # Deursloten
│   ├── beweging_sensor.py  # Bewegingssensoren
│   └── ...
├── woning/             # Huis logica
│   ├── smart_home.py   # Hoofdbesturing
│   ├── kamer.py        # Kamer beheer
│   └── ...
└── _site/              # Website weergave
    ├── index.html      # Status pagina
    └── style.css       # Opmaak
```

## Status Bekijken
Open in je browser:
```
_site/index.html
```
De pagina ververst automatisch elke 5 seconden om de laatste status te tonen.

## Gemaakt Door
Khaled Saada
AP Hogeschool, 2024-2025