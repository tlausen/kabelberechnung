package de.tlausen.kabelapp;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MainActivity extends Activity {

    private Spinner spTyp, spSystem, spModus;
    private EditText etStrom, etLeistung, etSpannung, etCos, etLaenge, etDuMax, etIk, etTk;
    private TextView tvErgebnis;
    private LinearLayout tableHeader, tableBody;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
    }

    private void buildUi() {
        ScrollView scroll = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(10);
        root.setPadding(pad, pad, pad, dp(20));
        scroll.addView(root);
        setContentView(scroll);

        TextView title = new TextView(this);
        title.setText("Kabelberechnung");
        title.setTextSize(22);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, dp(10));
        root.addView(title);

        spTyp = spinner(root, "Kabeltyp", namen().toArray(new String[0]));
        spSystem = spinner(root, "System", new String[]{"3~ Drehstrom", "1~ Wechselstrom"});
        spModus = spinner(root, "Lastvorgabe", new String[]{"Strom vorgeben", "Leistung vorgeben"});

        etStrom = feld(root, "Strom I (A)", "25");
        etLeistung = feld(root, "Leistung P (kW)", "10");
        etSpannung = feld(root, "Spannung U (V)", "400");
        etCos = feld(root, "cos φ", "0.9");
        etLaenge = feld(root, "Leitungslänge (m)", "50");
        etDuMax = feld(root, "max. Spannungsfall (%)", "4");

        List<String> temps = new ArrayList<>();
        for (double t : CableData.TEMP_FAKTOREN.keySet()) temps.add(String.valueOf((int) (double) t));
        LinearLayout tempRow = new LinearLayout(this);
        tempRow.setOrientation(LinearLayout.HORIZONTAL);
        root.addView(tempRow);
        TextView tLabel = label("Umgebungstemp. (°C)");
        tempRow.addView(tLabel, new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
        Spinner spTemp = new Spinner(this);
        spTemp.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item,
                temps.toArray(new String[0])));
        spTemp.setSelection(temps.indexOf("30"));
        tempRow.addView(spTemp, new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
        etTempHolder = spTemp;

        LinearLayout hRow = new LinearLayout(this);
        hRow.setOrientation(LinearLayout.HORIZONTAL);
        root.addView(hRow);
        hRow.addView(label("Häufung (Anzahl Kabel)"), new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
        Spinner spHauf = new Spinner(this);
        List<String> h = new ArrayList<>();
        for (int i = 1; i <= 9; i++) h.add(String.valueOf(i));
        spHauf.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item,
                h.toArray(new String[0])));
        hRow.addView(spHauf, new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
        etHaufHolder = spHauf;

        etIk = feld(root, "Kurzschlussstrom Ik (kA, optional)", "");
        etTk = feld(root, "Schaltzeit t (s)", "0.5");

        Button btn = new Button(this);
        btn.setText("Berechnen");
        btn.setOnClickListener(v -> berechne());
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        bp.topMargin = dp(12);
        bp.bottomMargin = dp(12);
        root.addView(btn, bp);

        tvErgebnis = new TextView(this);
        tvErgebnis.setTypeface(Typeface.MONOSPACE);
        tvErgebnis.setTextSize(13);
        tvErgebnis.setPadding(dp(6), dp(6), dp(6), dp(6));
        tvErgebnis.setBackgroundColor(Color.rgb(240, 240, 240));
        root.addView(tvErgebnis, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));

        TextView tabTitle = new TextView(this);
        tabTitle.setText("Querschnittsprüfung");
        tabTitle.setTypeface(Typeface.DEFAULT_BOLD);
        tabTitle.setPadding(0, dp(14), 0, dp(4));
        root.addView(tabTitle);

        tableBody = new LinearLayout(this);
        tableBody.setOrientation(LinearLayout.VERTICAL);
        root.addView(tableBody, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
    }

    private Spinner etTempHolder, etHaufHolder;

    private List<String> namen() {
        List<String> n = new ArrayList<>();
        for (CableData.Kabeltyp k : CableData.TYPEN) n.add(k.name);
        return n;
    }

    private Spinner spinner(LinearLayout root, String caption, String[] werte) {
        TextView lbl = label(caption);
        root.addView(lbl);
        Spinner sp = new Spinner(this);
        sp.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item,
                werte));
        root.addView(sp, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        return sp;
    }

    private EditText feld(LinearLayout root, String caption, String vorgabe) {
        root.addView(label(caption));
        EditText et = new EditText(this);
        et.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
        et.setText(vorgabe);
        root.addView(et, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        return et;
    }

    private TextView label(String text) {
        TextView tv = new TextView(this);
        tv.setText(text);
        tv.setPadding(0, dp(6), 0, 0);
        return tv;
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }

    private double num(EditText et) {
        String s = et.getText().toString().replace(',', '.').trim();
        if (s.isEmpty()) return 0;
        return Double.parseDouble(s);
    }

    private void berechne() {
        try {
            berechneInner();
        } catch (Exception e) {
            Toast.makeText(this, "Fehler: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void berechneInner() {
        CableData.Kabeltyp typ = CableData.TYPEN.get(spTyp.getSelectedItemPosition());
        boolean drehstrom = spSystem.getSelectedItemPosition() == 0;
        double u = num(etSpannung);
        double cosPhi = num(etCos);
        double laenge = num(etLaenge);
        double duMax = num(etDuMax);
        double rho = CableData.RHO.get(typ.material);
        if (u <= 0 || cosPhi <= 0 || laenge < 0 || duMax <= 0) {
            throw new IllegalArgumentException("Bitte alle Eingaben prüfen");
        }

        double strom;
        if (spModus.getSelectedItemPosition() == 1) {
            double p = num(etLeistung) * 1000;
            strom = drehstrom ? Calc.laststromDrehstrom(p, u, cosPhi)
                    : Calc.laststromWechselstrom(p, u, cosPhi);
        } else {
            strom = num(etStrom);
        }
        if (strom <= 0) throw new IllegalArgumentException("Der Laststrom muss größer 0 sein");

        double temp = Double.parseDouble((String) etTempHolder.getSelectedItem());
        double tf = CableData.tempFaktor(temp);
        double hf = CableData.haeufungFaktor(Integer.parseInt((String) etHaufHolder.getSelectedItem()));

        double ikA = num(etIk) * 1000;
        double tS = num(etTk);
        String isolation = typ.name.contains("2XS") || typ.name.contains("2XY") ? "XLPE" : "PVC";
        double k = CableData.kurzschlussK(typ.material, isolation);

        List<Double> qs = new ArrayList<>(typ.belastbarkeit.keySet());
        Double vorschlagBel = null;
        for (double q : qs) {
            if (typ.belastbarkeit.get(q) * tf * hf >= strom) {
                vorschlagBel = q;
                break;
            }
        }
        Double vorschlagSf = Calc.mindestquerschnittSpannungsfall(strom, laenge, u, rho,
                drehstrom, cosPhi, duMax, qs);
        Double vorschlag = null;
        if (vorschlagBel != null && vorschlagSf != null) vorschlag = Math.max(vorschlagBel, vorschlagSf);
        else if (vorschlagBel != null) vorschlag = vorschlagBel;
        else if (vorschlagSf != null) vorschlag = vorschlagSf;

        StringBuilder sb = new StringBuilder();
        sb.append(String.format(Locale.GERMANY, "%s\nSystem: %s | U = %g V | I = %.1f A\n",
                typ.name, drehstrom ? "3~" : "1~", u, strom));
        sb.append(String.format(Locale.GERMANY, "Länge = %g m | max. Δu = %g %%\n", laenge, duMax));
        sb.append(String.format(Locale.GERMANY, "Faktoren: Temperatur %.2f, Häufung %.2f\n", tf, hf));
        if (ikA > 0) {
            double sKs = Calc.querschnittKurzschluss(ikA, tS, k);
            sb.append(String.format(Locale.GERMANY,
                    "Kurzschluss: S_erf = %.1f mm² (Ik = %g kA, t = %g s, k = %g)\n",
                    sKs, ikA / 1000, tS, k));
        }
        sb.append("\n");
        if (vorschlag != null) {
            double iRed = typ.belastbarkeit.get(vorschlag) * tf * hf;
            double du = Calc.spannungsfallPct(strom, laenge, vorschlag, u, rho, drehstrom, cosPhi, 0.08);
            sb.append(String.format(Locale.GERMANY,
                    "→ Empfohlen: %g mm²\n   Belastbar (red.): %.0f A (%.0f %% Ausnutzung)\n   Δu = %.2f %%\n",
                    vorschlag, iRed, strom / iRed * 100, du));
            if (ikA > 0 && vorschlag < Calc.querschnittKurzschluss(ikA, tS, k)) {
                sb.append("   ⚠ Kurzschlussfestigkeit NICHT erfüllt!\n");
            }
        } else {
            sb.append("→ Kein Querschnitt erfüllt die Anforderungen.\n");
        }
        tvErgebnis.setText(sb.toString());

        tableBody.removeAllViews();
        for (double q : qs) {
            double iNenn = typ.belastbarkeit.get(q);
            double iRed = iNenn * tf * hf;
            double du = Calc.spannungsfallPct(strom, laenge, q, u, rho, drehstrom, cosPhi, 0.08);
            boolean okBel = iRed >= strom;
            boolean okSf = du <= duMax;
            String status = okBel && okSf ? "✓ geeignet"
                    : (okBel ? "✗ Δu" : "✗ Belastbarkeit");
            String line = String.format(Locale.GERMANY,
                    "%6g mm²  %6.0f A  →  %6.0f A   Δu %5.2f %%   %s",
                    q, iNenn, iRed, du, status);
            TextView row = new TextView(this);
            row.setTypeface(Typeface.MONOSPACE);
            row.setTextSize(12);
            row.setText(line);
            row.setPadding(dp(4), dp(2), dp(4), dp(2));
            row.setBackgroundColor(okBel && okSf ? Color.rgb(220, 245, 220)
                    : (okBel ? Color.rgb(255, 240, 220) : Color.rgb(255, 225, 225)));
            tableBody.addView(row);
        }
    }
}
