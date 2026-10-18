#!/usr/bin/env python3
"""Rebuild the Project 04 data audit, Wilson intervals, and SVG with stdlib."""
from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("isolate_id", "organism", "antibiotic", "result")
Z_95 = 1.96


def wilson(successes: int, n: int, z: float = Z_95) -> tuple[float, float]:
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("Wilson interval requires 0 <= successes <= n and n > 0")
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def write_svg(rows: list[dict[str, object]], path: Path) -> None:
    x0, width = 500, 815
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 690" role="img" aria-labelledby="title desc">',
           '<title id="title">Wilson intervals for synthetic resistance proportions</title>',
           '<desc id="desc">Six synthetic organism-antibiotic groups with n equals two; wide 95 percent intervals.</desc>',
           '<rect width="100%" height="100%" fill="#fff"/>',
           '<text x="55" y="55" font-family="Arial" font-size="26" font-weight="700" fill="#153b52">Proportions de résistance et intervalles de Wilson</text>',
           '<text x="55" y="88" font-family="Arial" font-size="16" fill="#59686e">Données synthétiques · six couples · n=2 par couple · IC bilatéraux à 95 %</text>']
    for tick in (0, 25, 50, 75, 100):
        x = x0 + width * tick / 100
        out += [f'<line x1="{x:.1f}" y1="130" x2="{x:.1f}" y2="625" stroke="#d7e1e4"/>',
                f'<text x="{x:.1f}" y="120" text-anchor="middle" font-family="Arial" font-size="14" fill="#59686e">{tick}%</text>']
    for i, row in enumerate(rows):
        y = 175 + i * 75
        label = html.escape(f"{row['organism']} · {row['antibiotic']} (n={row['n_tested']})")
        lo, hi, p = float(row["wilson95_low_pct"]), float(row["wilson95_high_pct"]), float(row["resistant_pct"])
        xlo, xhi, xp = x0 + width * lo / 100, x0 + width * hi / 100, x0 + width * p / 100
        out += [f'<text x="482" y="{y + 5}" text-anchor="end" font-family="Arial" font-size="16" fill="#153b52">{label}</text>',
                f'<line x1="{xlo:.1f}" y1="{y}" x2="{xhi:.1f}" y2="{y}" stroke="#087e8b" stroke-width="5" stroke-linecap="round"/>',
                f'<line x1="{xlo:.1f}" y1="{y-10}" x2="{xlo:.1f}" y2="{y+10}" stroke="#087e8b" stroke-width="3"/>',
                f'<line x1="{xhi:.1f}" y1="{y-10}" x2="{xhi:.1f}" y2="{y+10}" stroke="#087e8b" stroke-width="3"/>',
                f'<circle cx="{xp:.1f}" cy="{y}" r="8" fill="#153b52"/>',
                f'<line x1="55" y1="{y+33}" x2="1345" y2="{y+33}" stroke="#d7e1e4"/>']
    out += ['<text x="907" y="660" text-anchor="middle" font-family="Arial" font-size="15" fill="#59686e">Proportion R avec bornes inférieure et supérieure de Wilson à 95 %</text>', '</svg>']
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "DEMO_SYNTHETIC_wilson.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(REQUIRED).issubset(reader.fieldnames):
            raise SystemExit(f"Input must contain columns: {', '.join(REQUIRED)}")
        records = list(reader)
    missing = {column: 0 for column in (reader.fieldnames or [])}
    issues, seen, groups = [], set(), defaultdict(Counter)
    for line, row in enumerate(records, start=2):
        for column in missing:
            if not (row.get(column) or "").strip(): missing[column] += 1
        isolate, organism, antibiotic = ((row.get(k) or "").strip() for k in ("isolate_id", "organism", "antibiotic"))
        result = (row.get("result") or "").strip().upper()
        if not isolate or not organism or not antibiotic or result not in {"S", "I", "R"}:
            issues.append({"row_number": line, "issue": "missing_or_invalid_required_value", "value": result, "isolate_id": isolate, "antibiotic": antibiotic}); continue
        key = (isolate, antibiotic)
        if key in seen:
            issues.append({"row_number": line, "issue": "duplicate_isolate_antibiotic", "value": result, "isolate_id": isolate, "antibiotic": antibiotic}); continue
        seen.add(key); groups[(organism, antibiotic)][result] += 1
    rows = []
    for (organism, antibiotic), tally in sorted(groups.items()):
        n, r = sum(tally.values()), tally["R"]
        lo, hi = wilson(r, n)
        rows.append({"organism": organism, "antibiotic": antibiotic, "n_tested": n, "resistant_n": r,
                     "intermediate_n": tally["I"], "susceptible_n": tally["S"], "resistant_pct": round(100 * r / n, 1),
                     "wilson95_low_pct": lo * 100, "wilson95_high_pct": hi * 100})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    headers = ["organism", "antibiotic", "n_tested", "resistant_n", "intermediate_n", "susceptible_n", "resistant_pct", "wilson95_low_pct", "wilson95_high_pct"]
    with (args.output_dir / "amr_estimates_with_wilson_ci.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers); writer.writeheader(); writer.writerows(rows)
    audit = {"rows_received": len(records), "rows_curated": sum(sum(t.values()) for t in groups.values()),
             "missing_by_column": missing, "duplicate_isolate_antibiotic_rows": sum(i["issue"] == "duplicate_isolate_antibiotic" for i in issues),
             "invalid_result_values": sorted({str(i["value"]) for i in issues if i["issue"] == "missing_or_invalid_required_value"}),
             "issue_rows": issues, "dataset_status": "synthetic demonstration; not clinical data"}
    (args.output_dir / "data_quality_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    write_svg(rows, args.output_dir / "amr_wilson_intervals.svg")
    print(f"Audited {len(records)} synthetic rows; exported {len(rows)} groups and Wilson intervals.")


if __name__ == "__main__":
    main()
