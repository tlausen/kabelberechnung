import math
from kabelapp import calc, db


def test_laststrom_drehstrom():
    assert math.isclose(calc.laststrom_drehstrom(10000, 400, 1.0), 10000 / (math.sqrt(3) * 400))


def test_spannungsfall_drehstrom():
    # 70 m, 25 A, 10 mm2 Cu, 400 V: du ~ 2.7 %
    du_v, du_pct = calc.spannungsfall(25, 70, 10, 400, 0.0178, "3~", 1.0, 0.0)
    assert du_pct > 0 and du_pct < 5


def test_kurzschlussquerschnitt():
    # Ik=10kA, t=0.5s, k=143 -> S ~ 49.5 mm2
    s = calc.querschnitt_kurzschluss(10000, 0.5, 143)
    assert 49 < s < 50


def test_db_roundtrip():
    conn = db.get_db()
    typen = db.alle_kabeltypen(conn)
    assert len(typen) == 14
    assert db.temp_faktor(conn, 30.0) == 1.0
    assert db.haeufung_faktor(conn, 3) == 0.79
    namen = [r['name'] for r in typen]
    assert 'NAYY 0,6/1 kV (Al)' in namen and 'NA2XS(F)2Y 12/20 kV (Al, MS)' in namen
