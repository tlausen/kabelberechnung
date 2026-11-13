"""Elektrotechnische Berechnungen: Spannungsfall, Drehstrom, Kurzschluss."""
import math


def laststrom_drehstrom(p_w: float, u_v: float, cos_phi: float) -> float:
    """Strom bei Drehstrom: I = P / (sqrt(3) * U * cos(phi))."""
    if p_w is None or u_v is None or cos_phi is None or u_v <= 0 or cos_phi <= 0:
        raise ValueError("Ungültige Eingaben für Laststrom.")
    return p_w / (math.sqrt(3) * u_v * cos_phi)


def laststrom_wechselstrom(p_w: float, u_v: float, cos_phi: float) -> float:
    """Strom bei Einphasen-Last: I = P / (U * cos(phi))."""
    if u_v <= 0 or cos_phi <= 0:
        raise ValueError("Ungültige Eingaben für Laststrom.")
    return p_w / (u_v * cos_phi)


def spannungsfall(strom_a: float, laenge_m: float, querschnitt_mm2: float,
                  u_v: float, material_rho: float, system: str = "3~",
                  cos_phi: float = 1.0, reaktanz_x: float = 0.08) -> tuple[float, float]:
    """Spannungsfall in % (Näherung, induktiver Anteil 0,08 Ohm/km).

    1~: du = 2 * L * I * (R' cos(phi) + X' sin(phi)) / U
    3~: du = sqrt(3) * L * I * (R' cos(phi) + X' sin(phi)) / U
    """
    if querschnitt_mm2 <= 0 or u_v <= 0:
        raise ValueError("Querschnitt und Spannung müssen > 0 sein.")
    r_ohm_km = material_rho * 1000 / querschnitt_mm2
    z = r_ohm_km * cos_phi + reaktanz_x * math.sin(math.acos(cos_phi))
    faktor = math.sqrt(3) if system == "3~" else 2
    du_v = faktor * (laenge_m / 1000) * strom_a * z
    return du_v, du_v / u_v * 100


def mindestquerschnitt_spannungsfall(strom_a: float, laenge_m: float, u_v: float,
                                     material_rho: float, system: str,
                                     cos_phi: float, du_max_pct: float,
                                     querschnitte: list[float],
                                     reaktanz_x: float = 0.08) -> float | None:
    """Kleinsten Querschnitt aus der Liste, der den Grenzwert einhält."""
    for q in sorted(querschnitte):
        _, pct = spannungsfall(strom_a, laenge_m, q, u_v, material_rho, system, cos_phi, reaktanz_x)
        if pct <= du_max_pct:
            return q
    return None


def querschnitt_kurzschluss(ik_a: float, t_s: float, k_wert: float) -> float:
    """Thermisch erforderlicher Querschnitt: S = Ik * sqrt(t) / k (VDE 0102)."""
    if t_s <= 0 or k_wert <= 0:
        raise ValueError("Schaltzeit und k-Faktor müssen > 0 sein.")
    return ik_a * math.sqrt(t_s) / k_wert


def belastbarkeit_reduziert(i_nenn: float, temp_faktor: float, haeufung_faktor: float) -> float:
    """Reduzierte Belastbarkeit nach Umgebungstemperatur und Häufung."""
    return i_nenn * temp_faktor * haeufung_faktor


def pruefe_querschnitt(querschnitt_mm2: float, i_last_a: float, i_belastbar_a: float,
                       ik_a: float = 0.0, t_s: float = 0.0, k_wert: float = 115.0) -> dict:
    """Prüfung Querschnitt gegen Belastbarkeit und ggf. Kurzschluss."""
    ergebnis = {
        "querschnitt": querschnitt_mm2,
        "belastbar": querschnitt_mm2 >= 0 and i_belastbar_a >= i_last_a,
        "i_belastbar": i_belastbar_a,
        "ausnutzung": i_last_a / i_belastbar_a if i_belastbar_a > 0 else None,
    }
    if ik_a > 0 and t_s > 0:
        s_erf = querschnitt_kurzschluss(ik_a, t_s, k_wert)
        ergebnis["s_kurzschluss_erf"] = s_erf
        ergebnis["kurzschluss_ok"] = querschnitt_mm2 >= s_erf
    return ergebnis
