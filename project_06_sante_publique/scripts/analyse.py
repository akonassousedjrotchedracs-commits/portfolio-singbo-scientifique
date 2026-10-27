"""Analyse descriptive des indicateurs de santé publique du Bénin (2000-2024).

Usage : python scripts/analyse.py
Lit data/indicateurs_bm.csv, écrit les tableaux et figures dans results/.
"""
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
INK, MUTED, GRID, BENIN, REGION = "#153b52", "#59686e", "#d7e1e4", "#c0392b", "#153b52"
SHORT = {
    "SH.MLR.INCD.P3": "Paludisme (cas / 1 000 à risque)",
    "SH.DYN.MORT": "Mortalité < 5 ans (‰ naissances)",
    "SH.IMM.IDPT": "Couverture DTC3 (%)",
    "SH.IMM.MEAS": "Couverture rougeole (%)",
}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": MUTED})


def load():
    series = defaultdict(dict)
    names = {}
    with (ROOT / "data/indicateurs_bm.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            series[(row["indicator_code"], row["country_code"])][int(row["year"])] = float(row["value"])
            names[row["country_code"]] = row["country"]
    return series, names


def annual_change(points):
    """Variation annuelle moyenne (%) : pente d'une régression log-linéaire."""
    years = sorted(points)
    xs = [y - years[0] for y in years]
    ys = [math.log(points[y]) for y in years]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return (math.exp(slope) - 1) * 100


def summary(series, names):
    rows = []
    for code in SHORT:
        for country in ("BEN", "TGO", "NGA", "BFA", "NER", "SSF"):
            s = series[(code, country)]
            recent = {y: v for y, v in s.items() if y >= 2015}
            rows.append({
                "indicateur": SHORT[code], "pays": names[country],
                "valeur_2000": round(s[2000], 1), "valeur_2015": round(s[2015], 1), "valeur_2024": round(s[2024], 1),
                "variation_2000_2024_pct": round((s[2024] / s[2000] - 1) * 100, 1),
                "variation_annuelle_2015_2024_pct": round(annual_change(recent), 2),
                "rapport_benin_region_2024": round(series[(code, "BEN")][2024] / series[(code, "SSF")][2024], 2) if country == "BEN" else "",
            })
    with (RESULTS / "synthese_indicateurs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def save(fig, name):
    fig.savefig(RESULTS / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def small_multiples(series, names):
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), sharex=True)
    for ax, code in zip(axes.flat, SHORT):
        for country in ("TGO", "NGA", "BFA", "NER"):
            s = series[(code, country)]
            ax.plot(list(s), list(s.values()), color="#b8c6cc", lw=1.2)
            ax.text(2024.4, s[2024], names[country], fontsize=7.5, color=MUTED, va="center")
        region = series[(code, "SSF")]
        ax.plot(list(region), list(region.values()), color=REGION, lw=1.8, ls="--", label="Afrique subsaharienne")
        benin = series[(code, "BEN")]
        ax.plot(list(benin), list(benin.values()), color=BENIN, lw=2.6, label="Bénin")
        ax.scatter([2024], [benin[2024]], color=BENIN, zorder=3)
        ax.annotate(f"{benin[2024]:.0f}", (2024, benin[2024]), xytext=(-6, 8), textcoords="offset points", ha="right", color=BENIN, fontweight="bold")
        if code in ("SH.IMM.IDPT", "SH.IMM.MEAS"):
            ax.axhline(90, color="#2f8f5b", lw=1, ls=":")
            ax.text(2000.3, 91.5, "cible IA2030 : 90 %", fontsize=7.5, color="#2f8f5b")
            ax.set_ylim(0, 100)
        else:
            ax.set_ylim(0, None)
        ax.set_title(SHORT[code], loc="left", color=INK, fontweight="bold")
        ax.yaxis.grid(True, color=GRID)
        ax.set_xlim(2000, 2027)
    axes[0, 0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle("Bénin, pays voisins et Afrique subsaharienne, 2000–2024 · données Banque mondiale (OMS, UNICEF, IGME)",
                 x=0.01, ha="left", color=MUTED, fontsize=9.5)
    fig.tight_layout()
    save(fig, "fig_tendances_benin_region.png")


def vaccination_gap(series):
    dtc3, measles = series[("SH.IMM.IDPT", "BEN")], series[("SH.IMM.MEAS", "BEN")]
    years = sorted(dtc3)
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.fill_between(years, [100] * len(years), [dtc3[y] for y in years], color="#f6dcd8", label="Enfants non couverts par le DTC3")
    ax.fill_between(years, [dtc3[y] for y in years], [measles[y] for y in years], color="#fbf0d6", label="Écart DTC3 – rougeole")
    ax.plot(years, [dtc3[y] for y in years], color=INK, lw=2.2, label="DTC3")
    ax.plot(years, [measles[y] for y in years], color=BENIN, lw=2.2, label="Rougeole (1re dose)")
    ax.axhline(90, color="#2f8f5b", lw=1, ls=":")
    ax.text(2000.2, 91.5, "cible 90 %", fontsize=8, color="#2f8f5b")
    ax.annotate("", xy=(2024, 30), xytext=(2016, 30), arrowprops={"arrowstyle": "<->", "color": MUTED})
    ax.text(2020, 32, "rougeole : −24 points depuis 2016", ha="center", fontsize=8.5, color=MUTED)
    for y in (2016, 2024):
        ax.annotate(f"{measles[y]:.0f} %", (y, measles[y]), xytext=(0, -14), textcoords="offset points", ha="center", color=BENIN, fontsize=9, fontweight="bold")
    ax.set(ylim=(0, 100), xlim=(2000, 2024), ylabel="Couverture (%)")
    ax.yaxis.grid(True, color=GRID)
    ax.legend(frameon=False, fontsize=8.5, ncol=2, loc="lower left")
    ax.set_title("Bénin : couverture vaccinale des 12–23 mois (estimations OMS/UNICEF)", loc="left", color=INK, fontweight="bold")
    save(fig, "fig_vaccination_benin.png")


def ratio_to_region(series):
    fig, ax = plt.subplots(figsize=(11, 4.2))
    colours = {"SH.MLR.INCD.P3": "#8e44ad", "SH.DYN.MORT": "#d35400", "SH.IMM.IDPT": INK, "SH.IMM.MEAS": BENIN}
    for code, label in SHORT.items():
        b, r = series[(code, "BEN")], series[(code, "SSF")]
        years = sorted(set(b) & set(r))
        ratios = [b[y] / r[y] for y in years]
        ax.plot(years, ratios, color=colours[code], lw=2, label=label)
        ax.text(2024.3, ratios[-1], f"{ratios[-1]:.2f}", color=colours[code], va="center", fontsize=9, fontweight="bold")
    ax.axhline(1, color=MUTED, lw=1)
    ax.text(2000.2, 1.03, "niveau régional", fontsize=8, color=MUTED)
    ax.set(xlim=(2000, 2026), ylabel="Bénin / Afrique subsaharienne")
    ax.yaxis.grid(True, color=GRID)
    ax.legend(frameon=False, fontsize=8.5, ncol=2, loc="upper left")
    ax.set_title("Écart à la moyenne régionale (rapport > 1 : valeur plus élevée au Bénin)", loc="left", color=INK, fontweight="bold")
    save(fig, "fig_rapport_region.png")


def main():
    RESULTS.mkdir(exist_ok=True)
    series, names = load()
    rows = summary(series, names)
    small_multiples(series, names)
    vaccination_gap(series)
    ratio_to_region(series)
    for row in rows:
        if row["pays"] == "Bénin":
            print(row)


if __name__ == "__main__":
    main()
