package de.tlausen.kabelapp;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/** Kabelkennwerte nach VDE 0298-4 (30 °C, Verlegeart C). */
public final class CableData {

    public static final class Kabeltyp {
        public final String name;
        public final String material;
        public final double spannungKv;
        public final TreeMap<Double, Double> belastbarkeit;

        Kabeltyp(String name, String material, double spannungKv, double[][] werte) {
            this.name = name;
            this.material = material;
            this.spannungKv = spannungKv;
            this.belastbarkeit = new TreeMap<>();
            for (double[] w : werte) {
                belastbarkeit.put(w[0], w[1]);
            }
        }
    }

    public static final List<Kabeltyp> TYPEN = new ArrayList<>();

    static {
        TYPEN.add(new Kabeltyp("NYY-J 0,6/1 kV (Cu)", "Cu", 1.0, new double[][]{
                {1.5, 19.5}, {2.5, 27}, {4, 36}, {6, 46}, {10, 63}, {16, 85}, {25, 112},
                {35, 138}, {50, 168}, {70, 213}, {95, 258}, {120, 299}, {150, 344},
                {185, 392}, {240, 461}, {300, 530}, {400, 634}}));
        TYPEN.add(new Kabeltyp("NYM-J 300/500 V (Cu)", "Cu", 0.5, new double[][]{
                {1.5, 19.5}, {2.5, 27}, {4, 36}, {6, 46}, {10, 63}, {16, 85}, {25, 112},
                {35, 138}, {50, 168}}));
        TYPEN.add(new Kabeltyp("H07VK (Cu, Einzeldraht in Rohr)", "Cu", 1.0, new double[][]{
                {1.5, 24}, {2.5, 32}, {4, 42}, {6, 54}, {10, 73}, {16, 98}, {25, 129},
                {35, 158}, {50, 192}, {70, 245}, {95, 293}, {120, 339}, {150, 389},
                {185, 444}, {240, 522}, {300, 600}}));
        TYPEN.add(new Kabeltyp("H07RN-F (Cu, Gummischlauchleitung)", "Cu", 1.0, new double[][]{
                {1.5, 20}, {2.5, 28}, {4, 38}, {6, 50}, {10, 68}, {16, 89}, {25, 118},
                {35, 144}, {50, 171}, {70, 213}, {95, 258}, {120, 299}, {150, 344},
                {185, 392}, {240, 461}}));
        TYPEN.add(new Kabeltyp("NAYY 0,6/1 kV (Al)", "Al", 1.0, new double[][]{
                {16, 66}, {25, 88}, {35, 110}, {50, 132}, {70, 168}, {95, 204},
                {120, 238}, {150, 274}, {185, 314}, {240, 370}, {300, 426}, {400, 512}}));
        TYPEN.add(new Kabeltyp("NAYCWY 0,6/1 kV (Al, 4-leadrig)", "Al", 1.0, new double[][]{
                {16, 62}, {25, 82}, {35, 100}, {50, 121}, {70, 155}, {95, 188},
                {120, 221}, {150, 254}, {185, 291}, {240, 343}, {300, 394}, {400, 465}}));
        TYPEN.add(new Kabeltyp("NA2XY-J 0,6/1 kV (Al, XLPE)", "Al", 1.0, new double[][]{
                {16, 76}, {25, 100}, {35, 125}, {50, 150}, {70, 190}, {95, 232},
                {120, 270}, {150, 310}, {185, 356}, {240, 420}, {300, 485}, {400, 580}}));
        TYPEN.add(new Kabeltyp("N2XSY 12/20 kV (Cu, MS)", "Cu", 20.0, new double[][]{
                {25, 130}, {35, 160}, {50, 190}, {70, 230}, {95, 280}, {120, 325},
                {150, 370}, {185, 420}, {240, 490}, {300, 555}, {400, 640}}));
        TYPEN.add(new Kabeltyp("N2XS2Y 12/20 kV (Cu, MS)", "Cu", 20.0, new double[][]{
                {25, 128}, {35, 157}, {50, 187}, {70, 226}, {95, 276}, {120, 320},
                {150, 365}, {185, 414}, {240, 483}, {300, 547}, {400, 630}}));
        TYPEN.add(new Kabeltyp("N2XS(F)2Y 12/20 kV (Cu, MS)", "Cu", 20.0, new double[][]{
                {25, 130}, {35, 160}, {50, 190}, {70, 230}, {95, 280}, {120, 325},
                {150, 370}, {185, 420}, {240, 490}, {300, 555}, {400, 640}}));
        TYPEN.add(new Kabeltyp("NA2XS2Y 12/20 kV (Al, MS)", "Al", 20.0, new double[][]{
                {25, 105}, {35, 130}, {50, 155}, {70, 190}, {95, 230}, {120, 265},
                {150, 300}, {185, 340}, {240, 400}, {300, 455}, {400, 535}}));
        TYPEN.add(new Kabeltyp("NA2XS(F)2Y 12/20 kV (Al, MS)", "Al", 20.0, new double[][]{
                {25, 110}, {35, 135}, {50, 160}, {70, 195}, {95, 235}, {120, 270},
                {150, 305}, {185, 345}, {240, 405}, {300, 460}, {400, 540}}));
        TYPEN.add(new Kabeltyp("NA2XS(F)2Y 6/10 kV (Al, MS)", "Al", 10.0, new double[][]{
                {25, 122}, {35, 150}, {50, 178}, {70, 216}, {95, 261}, {120, 299},
                {150, 338}, {185, 382}, {240, 449}, {300, 509}, {400, 598}}));
        TYPEN.add(new Kabeltyp("N2XS(F)2Y 6/10 kV (Cu, MS)", "Cu", 10.0, new double[][]{
                {25, 143}, {35, 176}, {50, 210}, {70, 254}, {95, 308}, {120, 357},
                {150, 407}, {185, 462}, {240, 539}, {300, 611}, {400, 705}}));
    }

    public static final Map<String, Double> RHO = new LinkedHashMap<>();

    static {
        RHO.put("Cu", 0.0178);
        RHO.put("Al", 0.0283);
    }

    public static final Map<Double, Double> TEMP_FAKTOREN = new TreeMap<>();

    static {
        double[][] f = {{10.0, 1.22}, {15.0, 1.17}, {20.0, 1.12}, {25.0, 1.06}, {30.0, 1.00},
                {35.0, 0.94}, {40.0, 0.87}, {45.0, 0.79}, {50.0, 0.71}, {55.0, 0.61}, {60.0, 0.50}};
        for (double[] x : f) TEMP_FAKTOREN.put(x[0], x[1]);
    }

    public static final Map<Integer, Double> HAEUFUNG = new TreeMap<>();

    static {
        double[][] f = {{1, 1.00}, {2, 0.85}, {3, 0.79}, {4, 0.75}, {5, 0.73},
                {6, 0.72}, {7, 0.72}, {8, 0.71}, {9, 0.70}};
        for (double[] x : f) HAEUFUNG.put((int) x[0], x[1]);
    }

    public static double kurzschlussK(String material, String isolation) {
        if ("Cu".equals(material)) return "XLPE".equals(isolation) ? 143 : 115;
        return "XLPE".equals(isolation) ? 94 : 76;
    }

    public static double tempFaktor(double tempC) {
        TreeMap<Double, Double> m = (TreeMap<Double, Double>) TEMP_FAKTOREN;
        Map.Entry<Double, Double> lo = m.floorEntry(tempC);
        Map.Entry<Double, Double> hi = m.ceilingEntry(tempC);
        if (lo == null) return m.firstEntry().getValue();
        if (hi == null) return m.lastEntry().getValue();
        if (lo.getKey().equals(hi.getKey())) return lo.getValue();
        double t = (tempC - lo.getKey()) / (hi.getKey() - lo.getKey());
        return lo.getValue() + (hi.getValue() - lo.getValue()) * t;
    }

    public static double haeufungFaktor(int anzahl) {
        Double f = HAEUFUNG.get(anzahl);
        return f != null ? f : HAEUFUNG.get(9);
    }

    private CableData() {
    }
}
