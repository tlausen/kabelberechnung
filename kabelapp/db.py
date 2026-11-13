"""SQLite-Datenbank mit Kabelkennwerten (VDE 0298-4 / DIN VDE 0276)."""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kabel.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS kabeltyp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    material TEXT NOT NULL CHECK (material IN ('Cu', 'Al')),
    spannung_kv REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS belastbarkeit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kabeltyp_id INTEGER NOT NULL REFERENCES kabeltyp(id),
    querschnitt_mm2 REAL NOT NULL,
    strom_a REAL NOT NULL,
    UNIQUE (kabeltyp_id, querschnitt_mm2)
);

CREATE TABLE IF NOT EXISTS material (
    kuerzel TEXT PRIMARY KEY,
    rho_ohm_mm2_m REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS temp_faktor (
    temp_c REAL PRIMARY KEY,
    faktor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS haeufung_faktor (
    anzahl INTEGER PRIMARY KEY,
    faktor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS kurzschluss_k (
    material TEXT NOT NULL,
    isolation TEXT NOT NULL,
    k_wert REAL NOT NULL,
    PRIMARY KEY (material, isolation)
);
"""

# Belastbarkeit A bei 30 °C Umgebung, Verlegeart C (VDE 0298-4 Tabelle, Mehrleiterkabel)
BELASTBARKEIT = {
    # --- Niederspannung, Cu ---
    "NYY-J 0,6/1 kV (Cu)": {
        "material": "Cu", "spannung_kv": 1.0,
        "werte": {1.5: 19.5, 2.5: 27, 4: 36, 6: 46, 10: 63, 16: 85, 25: 112,
                  35: 138, 50: 168, 70: 213, 95: 258, 120: 299, 150: 344,
                  185: 392, 240: 461, 300: 530, 400: 634},
    },
    "NYM-J 300/500 V (Cu)": {
        "material": "Cu", "spannung_kv": 0.5,
        "werte": {1.5: 19.5, 2.5: 27, 4: 36, 6: 46, 10: 63, 16: 85, 25: 112,
                  35: 138, 50: 168},
    },
    "H07VK (Cu, Einzeldraht in Rohr)": {
        "material": "Cu", "spannung_kv": 1.0,
        "werte": {1.5: 24, 2.5: 32, 4: 42, 6: 54, 10: 73, 16: 98, 25: 129,
                  35: 158, 50: 192, 70: 245, 95: 293, 120: 339, 150: 389,
                  185: 444, 240: 522, 300: 600},
    },
    "H07RN-F (Cu, Gummischlauchleitung)": {
        "material": "Cu", "spannung_kv": 1.0,
        "werte": {1.5: 20, 2.5: 28, 4: 38, 6: 50, 10: 68, 16: 89, 25: 118,
                  35: 144, 50: 171, 70: 213, 95: 258, 120: 299, 150: 344,
                  185: 392, 240: 461},
    },
    # --- Niederspannung, Al ---
    "NAYY 0,6/1 kV (Al)": {
        "material": "Al", "spannung_kv": 1.0,
        "werte": {16: 66, 25: 88, 35: 110, 50: 132, 70: 168, 95: 204,
                  120: 238, 150: 274, 185: 314, 240: 370, 300: 426, 400: 512},
    },
    "NAYCWY 0,6/1 kV (Al, 4-leadrig)": {
        "material": "Al", "spannung_kv": 1.0,
        "werte": {16: 62, 25: 82, 35: 100, 50: 121, 70: 155, 95: 188,
                  120: 221, 150: 254, 185: 291, 240: 343, 300: 394, 400: 465},
    },
    "NA2XY-J 0,6/1 kV (Al, XLPE)": {
        "material": "Al", "spannung_kv": 1.0,
        "werte": {16: 76, 25: 100, 35: 125, 50: 150, 70: 190, 95: 232,
                  120: 270, 150: 310, 185: 356, 240: 420, 300: 485, 400: 580},
    },
    # --- Mittelspannung, Cu (XLPE) ---
    "N2XSY 12/20 kV (Cu, MS)": {
        "material": "Cu", "spannung_kv": 20.0,
        "werte": {25: 130, 35: 160, 50: 190, 70: 230, 95: 280, 120: 325,
                  150: 370, 185: 420, 240: 490, 300: 555, 400: 640},
    },
    "N2XS2Y 12/20 kV (Cu, MS)": {
        "material": "Cu", "spannung_kv": 20.0,
        "werte": {25: 128, 35: 157, 50: 187, 70: 226, 95: 276, 120: 320,
                  150: 365, 185: 414, 240: 483, 300: 547, 400: 630},
    },
    "N2XS(F)2Y 12/20 kV (Cu, MS)": {
        "material": "Cu", "spannung_kv": 20.0,
        "werte": {25: 130, 35: 160, 50: 190, 70: 230, 95: 280, 120: 325,
                  150: 370, 185: 420, 240: 490, 300: 555, 400: 640},
    },
    # --- Mittelspannung, Al (XLPE) ---
    "NA2XS2Y 12/20 kV (Al, MS)": {
        "material": "Al", "spannung_kv": 20.0,
        "werte": {25: 105, 35: 130, 50: 155, 70: 190, 95: 230, 120: 265,
                  150: 300, 185: 340, 240: 400, 300: 455, 400: 535},
    },
    "NA2XS(F)2Y 12/20 kV (Al, MS)": {
        "material": "Al", "spannung_kv": 20.0,
        "werte": {25: 110, 35: 135, 50: 160, 70: 195, 95: 235, 120: 270,
                  150: 305, 185: 345, 240: 405, 300: 460, 400: 540},
    },
    "NA2XS(F)2Y 6/10 kV (Al, MS)": {
        "material": "Al", "spannung_kv": 10.0,
        "werte": {25: 122, 35: 150, 50: 178, 70: 216, 95: 261, 120: 299,
                  150: 338, 185: 382, 240: 449, 300: 509, 400: 598},
    },
    "N2XS(F)2Y 6/10 kV (Cu, MS)": {
        "material": "Cu", "spannung_kv": 10.0,
        "werte": {25: 143, 35: 176, 50: 210, 70: 254, 95: 308, 120: 357,
                  150: 407, 185: 462, 240: 539, 300: 611, 400: 705},
    },
}

MATERIAL = {"Cu": 0.0178, "Al": 0.0283}

TEMP_FAKTOREN = {10: 1.22, 15: 1.17, 20: 1.12, 25: 1.06, 30: 1.00,
                 35: 0.94, 40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61, 60: 0.50}

HAEUFUNG = {1: 1.00, 2: 0.85, 3: 0.79, 4: 0.75, 5: 0.73, 6: 0.72,
            7: 0.72, 8: 0.71, 9: 0.70}

KURZSCHLUSS_K = [
    ("Cu", "PVC", 115), ("Cu", "XLPE", 143),
    ("Al", "PVC", 76), ("Al", "XLPE", 94),
]


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _seed(conn)
    return conn


def _seed(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for name, kuerzel in MATERIAL.items():
        cur.execute("INSERT OR IGNORE INTO material VALUES (?, ?)", (name, kuerzel))
    for temp, faktor in TEMP_FAKTOREN.items():
        cur.execute("INSERT OR IGNORE INTO temp_faktor VALUES (?, ?)", (temp, faktor))
    for anzahl, faktor in HAEUFUNG.items():
        cur.execute("INSERT OR IGNORE INTO haeufung_faktor VALUES (?, ?)", (anzahl, faktor))
    for material, isolation, k in KURZSCHLUSS_K:
        cur.execute("INSERT OR IGNORE INTO kurzschluss_k VALUES (?, ?, ?)", (material, isolation, k))
    for name, typ in BELASTBARKEIT.items():
        cur.execute("INSERT OR IGNORE INTO kabeltyp (name, material, spannung_kv) VALUES (?, ?, ?)",
                    (name, typ["material"], typ["spannung_kv"]))
        typ_id = cur.execute("SELECT id FROM kabeltyp WHERE name = ?", (name,)).fetchone()[0]
        for q, i in typ["werte"].items():
            cur.execute("INSERT OR IGNORE INTO belastbarkeit (kabeltyp_id, querschnitt_mm2, strom_a) VALUES (?, ?, ?)", (typ_id, q, i))
    conn.commit()


def alle_kabeltypen(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM kabeltyp ORDER BY spannung_kv, name").fetchall()


def belastbarkeit_fuer(conn: sqlite3.Connection, kabeltyp_id: int) -> dict[float, float]:
    rows = conn.execute(
        "SELECT querschnitt_mm2, strom_a FROM belastbarkeit WHERE kabeltyp_id = ? ORDER BY querschnitt_mm2",
        (kabeltyp_id,)).fetchall()
    return {r["querschnitt_mm2"]: r["strom_a"] for r in rows}


def temp_faktor(conn: sqlite3.Connection, temp_c: float) -> float:
    row = conn.execute("SELECT faktor FROM temp_faktor WHERE temp_c = ?", (temp_c,)).fetchone()
    if row:
        return row[0]
    keys = [r[0] for r in conn.execute("SELECT temp_c FROM temp_faktor ORDER BY temp_c")]
    if temp_c < min(keys):
        return conn.execute("SELECT MAX(faktor) FROM temp_faktor").fetchone()[0]
    if temp_c > max(keys):
        return conn.execute("SELECT MIN(faktor) FROM temp_faktor").fetchone()[0]
    lower = max(k for k in keys if k <= temp_c)
    upper = min(k for k in keys if k >= temp_c)
    fl = conn.execute("SELECT faktor FROM temp_faktor WHERE temp_c = ?", (lower,)).fetchone()[0]
    fu = conn.execute("SELECT faktor FROM temp_faktor WHERE temp_c = ?", (upper,)).fetchone()[0]
    if lower == upper:
        return fl
    return fl + (fu - fl) * (temp_c - lower) / (upper - lower)


def haeufung_faktor(conn: sqlite3.Connection, anzahl: int) -> float:
    row = conn.execute("SELECT faktor FROM haeufung_faktor WHERE anzahl = ?", (anzahl,)).fetchone()
    if row:
        return row[0]
    return conn.execute("SELECT MIN(faktor) FROM haeufung_faktor").fetchone()[0]


def kurzschluss_k(conn: sqlite3.Connection, material: str, isolation: str) -> float:
    row = conn.execute("SELECT k_wert FROM kurzschluss_k WHERE material = ? AND isolation = ?",
                       (material, isolation)).fetchone()
    return row[0] if row else 115.0
