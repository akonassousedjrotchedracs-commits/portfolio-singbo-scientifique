"""Génère les figures du portfolio à partir des CSV de résultats (matplotlib).

Usage : python tools/make_figures.py
Toutes les figures sont calculées à partir des fichiers du dépôt ; la simulation
FASTQ utilise une graine fixe pour être reproductible.
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INK, MUTED, GRID = "#153b52", "#59686e", "#d7e1e4"
SIR = {"S": "#2f8f5b", "I": "#e0a526", "R": "#c0392b"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 100,
})


def read(path):
    with open(ROOT / path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def save(fig, path):
    fig.savefig(ROOT / path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("écrit", path)


def short(organism):
    genus, _, species = organism.partition(" ")
    return f"{genus[0]}. {species}"


def stacked_sir(rows, n_key, title, subtitle, path):
    rows = sorted(rows, key=lambda r: float(r["resistant_n"]) / float(r[n_key]))
    labels = [f"{short(r['organism'])} · {r['antibiotic']}  (n={r[n_key]})" for r in rows]
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(rows) + 1.6))
    left = np.zeros(len(rows))
    for cat, key in (("R", "resistant_n"), ("I", "intermediate_n"), ("S", "susceptible_n")):
        values = np.array([100 * float(r[key]) / float(r[n_key]) for r in rows])
        ax.barh(labels, values, left=left, color=SIR[cat], label={"R": "Résistant", "I": "Intermédiaire", "S": "Sensible"}[cat], height=0.7)
        for y, (v, l) in enumerate(zip(values, left)):
            if v >= 8:
                ax.text(l + v / 2, y, f"{v:.0f} %", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
        left += values
    ax.set_xlim(0, 100)
    ax.set_xlabel("Part des résultats (%)")
    ax.xaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    ax.legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False)
    fig.suptitle(title, x=0.01, ha="left", color=INK, fontweight="bold", y=1.06)
    ax.set_title(subtitle, loc="left", color=MUTED, fontsize=9, pad=26)
    save(fig, path)


def project_01():
    stacked_sir(read("project_01_antimicrobial_resistance/results/amr_summary.csv"), "n_records",
                "Profils S/I/R par couple organisme–antibiotique",
                "100 observations synthétiques · tri par part de résistance",
                "project_01_antimicrobial_resistance/results/fig_sir_profiles.png")


def project_03():
    stacked_sir(read("project_03_sql_advanced/results/sql_amr_summary.csv"), "n_tested",
                "Agrégation SQL : profils S/I/R",
                "191 observations synthétiques chargées dans SQLite",
                "project_03_sql_advanced/results/fig_sql_sir_profiles.png")


def project_04():
    rows = read("project_04_advanced_biomedical_analysis/results/amr_estimates_with_wilson_ci.csv")
    rows = sorted(rows, key=lambda r: float(r["resistant_pct"]))
    fig, ax = plt.subplots(figsize=(9, 0.55 * len(rows) + 1.6))
    for y, r in enumerate(rows):
        p, lo, hi = float(r["resistant_pct"]), float(r["wilson95_low_pct"]), float(r["wilson95_high_pct"])
        ax.plot([lo, hi], [y, y], color=INK, lw=2.2, solid_capstyle="round")
        ax.plot([lo, lo], [y - .15, y + .15], color=INK, lw=1.5)
        ax.plot([hi, hi], [y - .15, y + .15], color=INK, lw=1.5)
        ax.plot(p, y, "s", color=SIR["R"], ms=8, zorder=3)
        ax.text(101, y, f"{p:.0f} % [{lo:.1f} ; {hi:.1f}]  {r['resistant_n']}/{r['n_tested']}", va="center", fontsize=8.5, color=MUTED)
    ax.set_yticks(range(len(rows)), [f"{short(r['organism'])} · {r['antibiotic']}" for r in rows])
    ax.set_xlim(0, 100)
    ax.set_ylim(-.7, len(rows) - .3)
    ax.set_xlabel("Proportion de résistance (%) et IC de Wilson à 95 %")
    ax.xaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    fig.suptitle("Résistance estimée et incertitude (Wilson 95 %)", x=0.01, ha="left", color=INK, fontweight="bold")
    save(fig, "project_04_advanced_biomedical_analysis/results/fig_wilson_forest.png")


def project_02():
    """Profil de qualité type FastQC sur une simulation Illumina 2×150 reproductible."""
    rng = np.random.default_rng(2027)
    n_reads, length = 5000, 150
    cycles = np.arange(1, length + 1)
    # Qualité moyenne : léger creux initial, plateau puis déclin en fin de lecture.
    mean = 36.5 - 2.5 * np.exp(-cycles / 3) - 9 * (cycles / length) ** 3.2
    sd = 1.2 + 4.5 * (cycles / length) ** 2.5
    # Effet lecture : la plupart des lectures sont bonnes, une minorité est dégradée.
    read_shift = rng.normal(0, 1.2, size=(n_reads, 1)) - rng.exponential(1.0, size=(n_reads, 1)) * (rng.random((n_reads, 1)) < .08) * 8
    quality = np.clip(rng.normal(mean + read_shift, sd, size=(n_reads, length)).round(), 2, 41)
    q = np.percentile(quality, [10, 25, 50, 75, 90], axis=0)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [2.3, 1]})
    for lo, hi, colour in ((28, 42, "#e3f2e6"), (20, 28, "#fbf0d6"), (0, 20, "#f6dcd8")):
        ax.axhspan(lo, hi, color=colour, zorder=0)
    ax.fill_between(cycles, q[0], q[4], color="#9cc5d1", alpha=.55, label="10e–90e percentile")
    ax.fill_between(cycles, q[1], q[3], color="#087e8b", alpha=.55, label="Interquartile")
    ax.plot(cycles, q[2], color=INK, lw=1.4, label="Médiane")
    ax.plot(cycles, quality.mean(axis=0), color=SIR["R"], lw=1.2, ls="--", label="Moyenne")
    ax.set(xlim=(1, length), ylim=(0, 42), xlabel="Position dans la lecture (cycle)", ylabel="Score Phred")
    ax.legend(loc="lower left", fontsize=8.5, frameon=False)
    ax.set_title("Qualité par cycle", loc="left", color=INK, fontweight="bold")
    per_read = quality.mean(axis=1)
    bx.hist(per_read, bins=40, color="#087e8b", edgecolor="white")
    bx.axvline(30, color=SIR["R"], ls="--", lw=1)
    q30 = (quality >= 30).mean() * 100
    bx.set(xlabel="Qualité moyenne par lecture", ylabel="Lectures")
    bx.set_title(f"Distribution · Q30 = {q30:.1f} % des bases", loc="left", color=INK, fontweight="bold")
    fig.suptitle(f"Simulation reproductible de {n_reads} lectures Illumina 2×150 (graine 2027)", x=0.01, ha="left", color=MUTED, fontsize=9.5)
    fig.tight_layout()
    save(fig, "project_02_bacterial_sequence/results/fig_fastq_quality_profile.png")

    rows = read("project_02_bacterial_sequence/results/sequence_qc.csv")
    fig, ax = plt.subplots(figsize=(7, 3))
    names = [r["sequence_id"].split("|")[0].replace("DEMO_SYNTHETIC_", "") for r in rows]
    gc = [float(r["gc_percent"]) for r in rows]
    ax.bar(names, gc, color="#087e8b", width=.55)
    for i, (g, r) in enumerate(zip(gc, rows)):
        ax.text(i, g / 2, f"{g:.1f} %\n{r['length_bp']} pb", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    ax.axhline(50.8, color=SIR["R"], ls="--", lw=1)
    ax.text(-.3, 52.5, "référence E. coli K-12 ≈ 50,8 %", ha="left", fontsize=8, color=SIR["R"])
    ax.set(ylim=(0, 70), ylabel="GC (%)")
    ax.set_title("Contenu GC des séquences FASTA contrôlées", loc="left", color=INK, fontweight="bold")
    save(fig, "project_02_bacterial_sequence/results/fig_gc_content.png")


if __name__ == "__main__":
    project_01()
    project_02()
    project_03()
    project_04()
