package de.tlausen.kabelapp;

import java.util.List;

/** Elektrotechnische Berechnungen (identisch zum Desktop-Tool). */
public final class Calc {

    public static double laststromDrehstrom(double pW, double uV, double cosPhi) {
        if (uV <= 0 || cosPhi <= 0) throw new IllegalArgumentException("Ungültige Eingaben");
        return pW / (Math.sqrt(3) * uV * cosPhi);
    }

    public static double laststromWechselstrom(double pW, double uV, double cosPhi) {
        if (uV <= 0 || cosPhi <= 0) throw new IllegalArgumentException("Ungültige Eingaben");
        return pW / (uV * cosPhi);
    }

    /** Spannungsfall in % (Näherung, induktiver Anteil 0,08 Ohm/km). */
    public static double spannungsfallPct(double stromA, double laengeM, double querschnittMm2,
                                         double uV, double rho, boolean drehstrom,
                                         double cosPhi, double reaktanzX) {
        if (querschnittMm2 <= 0 || uV <= 0) throw new IllegalArgumentException("Ungültige Eingaben");
        double rOhmKm = rho * 1000 / querschnittMm2;
        double z = rOhmKm * cosPhi + reaktanzX * Math.sin(Math.acos(cosPhi));
        double faktor = drehstrom ? Math.sqrt(3) : 2;
        double duV = faktor * (laengeM / 1000) * stromA * z;
        return duV / uV * 100;
    }

    public static Double mindestquerschnittSpannungsfall(double stromA, double laengeM, double uV,
                                                         double rho, boolean drehstrom,
                                                         double cosPhi, double duMaxPct,
                                                         List<Double> querschnitte) {
        for (double q : querschnitte) {
            if (spannungsfallPct(stromA, laengeM, q, uV, rho, drehstrom, cosPhi, 0.08) <= duMaxPct) {
                return q;
            }
        }
        return null;
    }

    /** Thermisch erforderlicher Querschnitt: S = Ik * sqrt(t) / k. */
    public static double querschnittKurzschluss(double ikA, double tS, double k) {
        if (tS <= 0 || k <= 0) throw new IllegalArgumentException("Ungültige Eingaben");
        return ikA * Math.sqrt(tS) / k;
    }

    private Calc() {
    }
}
