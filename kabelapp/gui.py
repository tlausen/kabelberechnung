"""Tkinter-Oberfläche für das Kabelberechnungs-Tool."""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from . import calc, db


class KabelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kabelberechnung – Strombelastbarkeit & Spannungsfall")
        self.geometry("820x680")
        self.conn = db.get_db()
        self.kabeltypen = {r["name"]: r for r in db.alle_kabeltypen(self.conn)}
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 6, "pady": 3}
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Eingaben ---
        eing = ttk.LabelFrame(frame, text="Eingaben")
        eing.pack(fill="x", **pad)

        self.var_typ = tk.StringVar()
        ttk.Label(eing, text="Kabeltyp:").grid(row=0, column=0, sticky="w", **pad)
        cb = ttk.Combobox(eing, textvariable=self.var_typ, state="readonly",
                          values=list(self.kabeltypen.keys()))
        cb.grid(row=0, column=1, columnspan=3, sticky="ew", **pad)
        cb.bind("<<ComboboxSelected>>", lambda e: self._lade_tabelle())

        self.var_system = tk.StringVar(value="3~ Drehstrom")
        ttk.Label(eing, text="System:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Combobox(eing, textvariable=self.var_system, state="readonly",
                     values=["3~ Drehstrom", "1~ Wechselstrom"]).grid(row=1, column=1, sticky="ew", **pad)

        self.var_modus = tk.StringVar(value="Strom vorgeben")
        ttk.Label(eing, text="Lastvorgabe:").grid(row=1, column=2, sticky="w", **pad)
        ttk.Combobox(eing, textvariable=self.var_modus, state="readonly",
                     values=["Strom vorgeben", "Leistung vorgeben"]).grid(row=1, column=3, sticky="ew", **pad)

        self.var_strom = tk.StringVar(value="")
        ttk.Label(eing, text="Strom I (A):").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_strom).grid(row=2, column=1, sticky="ew", **pad)

        self.var_leistung = tk.StringVar(value="")
        ttk.Label(eing, text="Leistung P (kW):").grid(row=2, column=2, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_leistung).grid(row=2, column=3, sticky="ew", **pad)

        self.var_spannung = tk.StringVar(value="400")
        ttk.Label(eing, text="Spannung U (V):").grid(row=3, column=0, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_spannung).grid(row=3, column=1, sticky="ew", **pad)

        self.var_cos = tk.StringVar(value="0.9")
        ttk.Label(eing, text="cos φ:").grid(row=3, column=2, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_cos).grid(row=3, column=3, sticky="ew", **pad)

        self.var_laenge = tk.StringVar(value="50")
        ttk.Label(eing, text="Leitungslänge (m):").grid(row=4, column=0, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_laenge).grid(row=4, column=1, sticky="ew", **pad)

        self.var_dumax = tk.StringVar(value="4")
        ttk.Label(eing, text="max. Spannungsfall (%):").grid(row=4, column=2, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_dumax).grid(row=4, column=3, sticky="ew", **pad)

        self.var_temp = tk.StringVar(value="30")
        ttk.Label(eing, text="Umgebungstemp. (°C):").grid(row=5, column=0, sticky="w", **pad)
        ttk.Combobox(eing, textvariable=self.var_temp, state="readonly",
                     values=["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]).grid(
            row=5, column=1, sticky="ew", **pad)

        self.var_haeufung = tk.StringVar(value="1")
        ttk.Label(eing, text="Häufung (Anzahl Kabel):").grid(row=5, column=2, sticky="w", **pad)
        ttk.Spinbox(eing, from_=1, to=9, textvariable=self.var_haeufung, width=6).grid(
            row=5, column=3, sticky="ew", **pad)

        self.var_ik = tk.StringVar(value="")
        ttk.Label(eing, text="Kurzschlussstrom Ik (kA, optional):").grid(row=6, column=0, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_ik).grid(row=6, column=1, sticky="ew", **pad)

        self.var_tk = tk.StringVar(value="0.5")
        ttk.Label(eing, text="Schaltzeit t (s):").grid(row=6, column=2, sticky="w", **pad)
        ttk.Entry(eing, textvariable=self.var_tk).grid(row=6, column=3, sticky="ew", **pad)

        eing.columnconfigure(1, weight=1)
        eing.columnconfigure(3, weight=1)

        ttk.Button(frame, text="Berechnen", command=self.berechne).pack(pady=8)

        # --- Ergebnisse ---
        erg = ttk.LabelFrame(frame, text="Ergebnis")
        erg.pack(fill="both", expand=True, **pad)
        self.txt_ergebnis = tk.Text(erg, height=12, wrap="word")
        self.txt_ergebnis.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Datenbanktabelle ---
        tab = ttk.LabelFrame(frame, text="Strombelastbarkeit des gewählten Kabeltyps (30 °C, Verlegeart C)")
        tab.pack(fill="both", expand=True, **pad)
        spalten = ("querschnitt", "nennstrom", "reduziert", "spannungsfall", "status")
        self.tree = ttk.Treeview(tab, columns=spalten, show="headings", height=8)
        for s, t in zip(spalten, ["Querschnitt (mm²)", "I_r Nenn (A)", "I_r reduziert (A)",
                                  "Spannungsfall (%)", "Bewertung"]):
            self.tree.heading(s, text=t)
            self.tree.column(s, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)
        self._lade_tabelle()

    def _lade_tabelle(self):
        self.tree.delete(*self.tree.get_children())
        typ = self.kabeltypen.get(self.var_typ.get())
        if not typ:
            return
        werte = db.belastbarkeit_fuer(self.conn, typ["id"])
        tf = db.temp_faktor(self.conn, float(self.var_temp.get() or 30))
        hf = db.haeufung_faktor(self.conn, int(self.var_haeufung.get() or 1))
        for q, i in werte.items():
            self.tree.insert("", "end", values=(q, i, round(i * tf * hf, 1), "", ""))

    def berechne(self):
        try:
            self._berechne()
        except (ValueError, KeyError) as e:
            messagebox.showerror("Fehler", str(e))

    def _berechne(self):
        typ = self.kabeltypen.get(self.var_typ.get())
        if not typ:
            raise ValueError("Bitte einen Kabeltyp auswählen.")
        u = float(self.var_spannung.get())
        cos_phi = float(self.var_cos.get())
        laenge = float(self.var_laenge.get())
        dumax = float(self.var_dumax.get())
        system = "3~" if self.var_system.get().startswith("3") else "1~"
        rho = db.MATERIAL[typ["material"]]

        if self.var_modus.get() == "Leistung vorgeben":
            p = float(self.var_leistung.get()) * 1000
            strom = (calc.laststrom_drehstrom if system == "3~" else calc.laststrom_wechselstrom)(
                p, u, cos_phi)
        else:
            strom = float(self.var_strom.get())
        if strom <= 0:
            raise ValueError("Der Laststrom muss größer 0 sein.")

        tf = db.temp_faktor(self.conn, float(self.var_temp.get() or 30))
        hf = db.haeufung_faktor(self.conn, int(self.var_haeufung.get() or 1))
        werte = db.belastbarkeit_fuer(self.conn, typ["id"])

        ik_a = float(self.var_ik.get()) * 1000 if self.var_ik.get() else 0.0
        t_s = float(self.var_tk.get() or 0)
        k_wert = db.kurzschluss_k(self.conn, typ["material"], "XLPE" if ("2XS" in typ["name"] or "2XY" in typ["name"]) else "PVC")

        vorschlag_bel = min((q for q, i in werte.items() if i * tf * hf >= strom), default=None)
        vorschlag_sf = calc.mindestquerschnitt_spannungsfall(
            strom, laenge, u, rho, system, cos_phi, dumax, list(werte.keys()))
        vorschlag = max(filter(None, [vorschlag_bel, vorschlag_sf]), default=None)

        zeilen = [f"Kabeltyp: {typ['name']}  |  System: {system}  |  U = {u:g} V  |  I = {strom:.1f} A"]
        if self.var_modus.get() == "Leistung vorgeben":
            zeilen.append(f"P = {float(self.var_leistung.get()):g} kW, cos φ = {cos_phi}")
        zeilen.append(f"Leitungslänge = {laenge:g} m, max. Spannungsfall = {dumax:g} %")
        zeilen.append(f"Reduktionsfaktoren: Temperatur {tf:.2f}, Häufung {hf:.2f}")
        if ik_a > 0:
            s_ks = calc.querschnitt_kurzschluss(ik_a, t_s, k_wert)
            zeilen.append(f"Kurzschluss: S_erf = {s_ks:.1f} mm² (Ik = {ik_a/1000:g} kA, t = {t_s:g} s, k = {k_wert:g})")
        zeilen.append("")
        if vorschlag:
            i_red = werte[vorschlag] * tf * hf
            _, du_pct = calc.spannungsfall(strom, laenge, vorschlag, u, rho, system, cos_phi)
            zeilen.append(f"→ Empfohlener Querschnitt: {vorschlag:g} mm²")
            zeilen.append(f"   Belastbarkeit (reduziert): {i_red:.0f} A ({strom/i_red*100:.0f} % Ausnutzung)")
            zeilen.append(f"   Spannungsfall: {du_pct:.2f} %")
            if ik_a > 0 and vorschlag < calc.querschnitt_kurzschluss(ik_a, t_s, k_wert):
                zeilen.append("   ⚠ Kurzschlussfestigkeit NICHT erfüllt – größerer Querschnitt wählen!")
        else:
            zeilen.append("→ Kein Querschnitt der Datenbank erfüllt die Anforderungen.")

        self.txt_ergebnis.delete("1.0", "end")
        self.txt_ergebnis.insert("1.0", "\n".join(zeilen))

        for row in self.tree.get_children():
            q = self.tree.set(row, "querschnitt")
            _, du_pct = calc.spannungsfall(strom, laenge, float(q), u, rho, system, cos_phi)
            self.tree.set(row, "spannungsfall", f"{du_pct:.2f}")
            ok_bel = werte[float(q)] * tf * hf >= strom
            ok_sf = du_pct <= dumax
            if ok_bel and ok_sf:
                status = "✓ geeignet"
            elif not ok_bel:
                status = "✗ Belastbarkeit"
            else:
                status = "✗ Spannungsfall"
            self.tree.set(row, "status", status)


def main():
    app = KabelApp()
    app.mainloop()
