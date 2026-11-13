# Kabelberechnung

Desktop-Tool (Python/Tkinter) für einfache Kabelberechnungen:

- **Kabel-Datenbank (SQLite)**: Strombelastbarkeit nach VDE 0298-4 (NYY, NYM, NYY-Al, NA2XY-J, N2XSY 12/20 kV)
- **Spannungsfall** 1~ und 3~ abhängig von Leitungslänge, Spannung, cos φ und Querschnitt
- **Drehstrom/Mittelspannung**: Laststrom aus P, U, cos φ; Querschnittsprüfung bei 10/20 kV
- **Reduktionsfaktoren**: Umgebungstemperatur und Häufung
- **Kurzschlussfestigkeit**: S = Ik · √t / k (VDE 0102)
- **Querschnittsvorschlag** aus Belastbarkeit UND Spannungsfall

## Start

```bash
python main.py
```

oder `python -m kabelapp`. Die SQLite-Datenbank `kabelapp/kabel.db` wird beim ersten Start automatisch erzeugt.

## Tests

```bash
python -m pytest kabelapp/test_calc.py
```

> Hinweis: Normwerte sind Näherungen aus VDE 0276/0298 – für die Ausführung gilt die konkrete Projektplanung durch eine Elektrofachkraft.
