#!/usr/bin/env python3
"""Rebuild Project 02 exploratory FASTA QC using only Python's standard library."""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = set("ACGT")
STOPS = {"TAA", "TAG", "TGA"}


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    name: str | None = None
    seq: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if name is not None:
                records.append((name, "".join(seq).upper()))
            name, seq = line[1:].strip(), []
            if not name:
                raise ValueError(f"Empty FASTA header at line {line_no}")
        elif name is None:
            raise ValueError(f"Sequence found before a FASTA header at line {line_no}")
        else:
            seq.append("".join(line.split()))
    if name is not None:
        records.append((name, "".join(seq).upper()))
    if not records or any(not sequence for _, sequence in records):
        raise ValueError("FASTA must contain at least one non-empty sequence")
    return records


def longest_simple_orf(sequence: str) -> int:
    longest = 0
    for frame in range(3):
        start: int | None = None
        for pos in range(frame, len(sequence) - 2, 3):
            codon = sequence[pos:pos + 3]
            if start is None and codon == "ATG":
                start = pos
            elif start is not None and codon in STOPS:
                longest = max(longest, pos + 3 - start)
                start = None
    return longest


def render_svg(rows: list[dict[str, object]], mean_gc: float, total_bp: int, ambiguous: int, path: Path) -> None:
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" role="img" aria-labelledby="title desc">',
           '<title id="title">Synthetic sequence quality-control overview</title>',
           '<desc id="desc">Lengths, GC fraction, and ambiguous base counts for three synthetic sequences.</desc>',
           '<rect width="100%" height="100%" fill="#f7fafc"/>',
           '<text x="42" y="48" font-family="Arial" font-size="25" font-weight="700" fill="#173b52">Contrôle qualité des séquences</text>',
           '<text x="42" y="78" font-family="Arial" font-size="14" fill="#587080">Démonstration synthétique · longueur en pb · contenu GC · bases ambiguës</text>']
    for i, row in enumerate(rows):
        y = 137 + i * 86
        name = html.escape(f"séquence {i + 1:02d}")
        length, gc, amb = int(row["length_bp"]), float(row["gc_percent"]), int(row["ambiguous_bases"])
        out += [f'<text x="42" y="{y}" font-family="Arial" font-size="16" font-weight="700" fill="#173b52">{name}</text>',
                f'<text x="42" y="{y + 24}" font-family="Arial" font-size="13" fill="#587080">{length} pb · {gc:.1f}% GC · {amb} base(s) ambiguë(s)</text>',
                f'<rect x="350" y="{y - 17}" width="480" height="20" rx="10" fill="#e3edf1"/>',
                f'<rect x="350" y="{y - 17}" width="{480 * gc / 100:.1f}" height="20" rx="10" fill="#0b8290"/>',
                f'<text x="850" y="{y}" font-family="Arial" font-size="14" font-weight="700" fill="#173b52">{gc:.1f}% GC</text>',
                f'<rect x="350" y="{y + 14}" width="{max(amb * 7, 4)}" height="8" rx="4" fill="{"#d18431" if amb else "#9ab7c0"}"/>']
    out += [f'<text x="42" y="405" font-family="Arial" font-size="13" fill="#587080">Sommaire : {len(rows)} séquences · {total_bp} pb · {ambiguous} bases ambiguës · GC moyen {mean_gc:.3f}%</text>', '</svg>']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "DEMO_SYNTHETIC_sequences.fasta")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    records = read_fasta(args.input)
    rows = []
    for name, sequence in records:
        valid_count = sum(base in VALID for base in sequence)
        gc_count = sum(base in {"G", "C"} for base in sequence)
        ambiguous = len(sequence) - valid_count
        rows.append({"sequence_id": name, "length_bp": len(sequence),
                     "gc_percent": round(gc_count * 100 / valid_count, 3) if valid_count else 0.0,
                     "ambiguous_bases": ambiguous, "ambiguous_percent": round(ambiguous * 100 / len(sequence), 3),
                     "longest_simple_orf_nt_forward_strand": longest_simple_orf(sequence),
                     "contains_non_acgt": str(ambiguous > 0)})
    total_bp = sum(int(row["length_bp"]) for row in rows)
    total_ambiguous = sum(int(row["ambiguous_bases"]) for row in rows)
    mean_length = round(total_bp / len(rows), 2)
    mean_gc = round(sum(float(row["gc_percent"]) for row in rows) / len(rows), 3)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    headers = ["sequence_id", "length_bp", "gc_percent", "ambiguous_bases", "ambiguous_percent", "longest_simple_orf_nt_forward_strand", "contains_non_acgt"]
    with (args.output_dir / "sequence_qc.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader(); writer.writerows(rows)
    summary = {"fasta_file": args.input.name, "n_sequences": len(rows), "total_bp": total_bp,
               "mean_length_bp": mean_length, "mean_gc_percent": mean_gc,
               "total_ambiguous_bases": total_ambiguous,
               "note": "Synthetic exploratory QC only; not species identification, assembly validation or formal annotation."}
    (args.output_dir / "sequence_qc_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    render_svg(rows, mean_gc, total_bp, total_ambiguous, args.output_dir / "sequence_qc_overview.svg")
    print(f"Rebuilt QC for {len(rows)} sequences ({total_bp} bp; {total_ambiguous} ambiguous bases).")


if __name__ == "__main__":
    main()
