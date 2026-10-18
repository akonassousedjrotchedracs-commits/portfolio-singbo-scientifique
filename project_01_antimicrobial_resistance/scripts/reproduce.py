#!/usr/bin/env python3
"""Rebuild the Project 01 summaries and SVG using Python's standard library."""
from __future__ import annotations

import argparse
import csv
import html
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("organism", "antibiotic", "result")


def write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def render_svg(rows: list[dict[str, object]], path: Path) -> None:
    width, height = 1200, 620
    x0, chart_width = 365, 755
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Synthetic antimicrobial resistance proportions</title>',
        '<desc id="desc">Five synthetic organism-antibiotic pairs with 20 records per pair.</desc>',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<text x="55" y="55" font-family="Arial" font-size="26" font-weight="700" fill="#153b52">Antimicrobial resistance proportions</text>',
        '<text x="55" y="88" font-family="Arial" font-size="16" fill="#59686e">Synthetic dataset · denominators shown · no clinical inference</text>',
    ]
    for tick in (0, 25, 50, 75, 100):
        x = x0 + chart_width * tick / 100
        out += [f'<line x1="{x:.1f}" y1="125" x2="{x:.1f}" y2="515" stroke="#d7e1e4"/>',
                f'<text x="{x:.1f}" y="118" text-anchor="middle" font-family="Arial" font-size="13" fill="#59686e">{tick}%</text>']
    for i, row in enumerate(rows):
        y = 165 + i * 77
        organism = html.escape(str(row["organism"]))
        antibiotic = html.escape(str(row["antibiotic"]))
        pct = float(row["resistant_pct"])
        n = int(row["n_records"])
        out += [f'<text x="347" y="{y + 6}" text-anchor="end" font-family="Arial" font-size="17" fill="#153b52">{organism} · {antibiotic}</text>',
                f'<rect x="{x0}" y="{y - 21}" width="{chart_width}" height="30" rx="4" fill="#eef6f7"/>',
                f'<rect x="{x0}" y="{y - 21}" width="{chart_width * pct / 100:.1f}" height="30" rx="4" fill="#087e8b"/>',
                f'<text x="{x0 + chart_width * pct / 100 + 10:.1f}" y="{y + 1}" font-family="Arial" font-size="15" font-weight="700" fill="#153b52">{pct:g}% (n={n})</text>',
                f'<line x1="55" y1="{y + 28}" x2="1145" y2="{y + 28}" stroke="#d7e1e4"/>']
    out += ['<text x="742" y="550" text-anchor="middle" font-family="Arial" font-size="15" fill="#59686e">Resistant results (R) / all classified tests in each synthetic pair</text>', '</svg>']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "results" / "amr_observations_synthetic_100.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise SystemExit(f"Input must contain columns: {', '.join(FIELDS)}")
        counts: dict[tuple[str, str], Counter[str]] = {}
        n_rows = 0
        for line, row in enumerate(reader, start=2):
            organism = (row.get("organism") or "").strip()
            antibiotic = (row.get("antibiotic") or "").strip()
            result = (row.get("result") or "").strip().upper()
            if not organism or not antibiotic or result not in {"S", "I", "R"}:
                raise SystemExit(f"Invalid or incomplete record at line {line}")
            counts.setdefault((organism, antibiotic), Counter())[result] += 1
            n_rows += 1
    if not n_rows:
        raise SystemExit("No observations found")
    summaries, categories = [], []
    for (organism, antibiotic), tally in sorted(counts.items()):
        n = sum(tally.values())
        summaries.append({"organism": organism, "antibiotic": antibiotic, "n_records": n,
                          "resistant_n": tally["R"], "intermediate_n": tally["I"], "susceptible_n": tally["S"],
                          "resistant_pct": round(tally["R"] * 100 / n, 1)})
        for category in ("R", "I", "S"):
            categories.append({"organism": organism, "antibiotic": antibiotic, "result": category, "n": tally[category]})
    write_csv(args.output_dir / "amr_summary.csv", ["organism", "antibiotic", "n_records", "resistant_n", "intermediate_n", "susceptible_n", "resistant_pct"], summaries)
    write_csv(args.output_dir / "result_counts.csv", ["organism", "antibiotic", "result", "n"], categories)
    render_svg(summaries, args.output_dir / "resistance_proportions.svg")
    print(f"Rebuilt summaries for {n_rows} observations across {len(summaries)} organism-antibiotic pairs.")


if __name__ == "__main__":
    main()
