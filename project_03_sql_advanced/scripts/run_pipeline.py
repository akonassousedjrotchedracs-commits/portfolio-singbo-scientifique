#!/usr/bin/env python3
"""Load synthetic AMR CSV into SQLite, audit it, and export SQL summaries."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = {"S", "I", "R"}


def write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers); writer.writeheader(); writer.writerows(rows)


def write_svg(path: Path, rows: list[dict[str, object]]) -> None:
    width, height, x0, plot = 1100, 180 + 76 * len(rows), 440, 560
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">',
           '<title id="t">Synthetic antimicrobial resistance summary from SQLite</title>',
           '<desc id="d">SQL aggregates for synthetic organism-antibiotic groups; 31–32 synthetic tests per group.</desc>',
           '<rect width="100%" height="100%" fill="#fff"/>',
           '<text x="45" y="48" font-family="Arial" font-size="25" font-weight="700" fill="#153b52">SQL summary · synthetic observations</text>',
           '<text x="45" y="78" font-family="Arial" font-size="15" fill="#59686e">Resistant results (R) / all classified tests · n=31–32 per pair</text>']
    for tick in (0,25,50,75,100):
        x=x0+plot*tick/100
        out.extend([f'<line x1="{x:.1f}" y1="110" x2="{x:.1f}" y2="{height-42}" stroke="#d7e1e4"/>',f'<text x="{x:.1f}" y="105" text-anchor="middle" font-family="Arial" font-size="12" fill="#59686e">{tick}%</text>'])
    for i,row in enumerate(rows):
        y=147+i*76; pct=float(row['resistant_pct']); label=html.escape(f"{row['organism']} - {row['antibiotic']}")
        out.extend([f'<text x="425" y="{y+5}" text-anchor="end" font-family="Arial" font-size="15" fill="#153b52">{label}</text>',f'<rect x="{x0}" y="{y-17}" width="{plot}" height="25" rx="3" fill="#eef6f7"/>',f'<rect x="{x0}" y="{y-17}" width="{plot*pct/100:.1f}" height="25" rx="3" fill="#087e8b"/>',f'<text x="{x0+plot*pct/100+8:.1f}" y="{y+1}" font-family="Arial" font-size="13" font-weight="700" fill="#153b52">{pct:g}% (n={row["n_tested"]})</text>'])
    out.append('</svg>')
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text("\n".join(out),encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "DEMO_SYNTHETIC_amr_sql.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--sql", type=Path, default=ROOT / "sql" / "summary.sql")
    args = parser.parse_args()
    raw_bytes = args.input.read_bytes()
    with args.input.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"isolate_id", "organism", "antibiotic", "result"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise SystemExit(f"Input must contain columns: {', '.join(sorted(required))}")
        records = list(reader)
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE organisms (organism_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
        CREATE TABLE antibiotics (antibiotic_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
        CREATE TABLE isolates (isolate_id TEXT PRIMARY KEY, organism_id INTEGER NOT NULL REFERENCES organisms);
        CREATE TABLE susceptibility_results (
            result_id INTEGER PRIMARY KEY,
            isolate_id TEXT NOT NULL REFERENCES isolates,
            antibiotic_id INTEGER NOT NULL REFERENCES antibiotics,
            result TEXT NOT NULL CHECK (result IN ('S','I','R')),
            UNIQUE (isolate_id, antibiotic_id)
        );
    """)
    issues: list[dict[str, object]] = []
    organism_by_isolate: dict[str, str] = {}
    inserted = 0
    for line, row in enumerate(records, start=2):
        isolate, organism = (row.get("isolate_id") or "").strip(), (row.get("organism") or "").strip()
        antibiotic, result = (row.get("antibiotic") or "").strip(), (row.get("result") or "").strip().upper()
        if not all((isolate, organism, antibiotic, result)):
            issues.append({"row_number": line, "issue": "missing_required_value", "value": "", "isolate_id": isolate, "antibiotic": antibiotic}); continue
        if result not in VALID:
            issues.append({"row_number": line, "issue": "invalid_result", "value": result, "isolate_id": isolate, "antibiotic": antibiotic}); continue
        if isolate in organism_by_isolate and organism_by_isolate[isolate] != organism:
            issues.append({"row_number": line, "issue": "isolate_organism_conflict", "value": organism, "isolate_id": isolate, "antibiotic": antibiotic}); continue
        try:
            organism_by_isolate[isolate] = organism
            conn.execute("INSERT OR IGNORE INTO organisms(name) VALUES (?)", (organism,))
            conn.execute("INSERT OR IGNORE INTO antibiotics(name) VALUES (?)", (antibiotic,))
            organism_id = conn.execute("SELECT organism_id FROM organisms WHERE name=?", (organism,)).fetchone()[0]
            conn.execute("INSERT OR IGNORE INTO isolates(isolate_id, organism_id) VALUES (?,?)", (isolate, organism_id))
            antibiotic_id = conn.execute("SELECT antibiotic_id FROM antibiotics WHERE name=?", (antibiotic,)).fetchone()[0]
            conn.execute("INSERT INTO susceptibility_results(isolate_id, antibiotic_id, result) VALUES (?,?,?)", (isolate, antibiotic_id, result))
            inserted += 1
        except sqlite3.IntegrityError:
            issues.append({"row_number": line, "issue": "duplicate_isolate_antibiotic", "value": result, "isolate_id": isolate, "antibiotic": antibiotic})
    summary_sql = args.sql.read_text(encoding="utf-8")
    summary_rows = [dict(zip([col[0] for col in conn.execute(summary_sql).description], row)) for row in conn.execute(summary_sql).fetchall()]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "sql_amr_summary.csv", ["organism", "antibiotic", "n_tested", "resistant_n", "intermediate_n", "susceptible_n", "resistant_pct"], summary_rows)
    write_csv(args.output_dir / "data_quality_issues.csv", ["row_number", "issue", "value", "isolate_id", "antibiotic"], issues)
    advanced_text = (ROOT / "sql" / "advanced_queries.sql").read_text(encoding="utf-8")
    statements, buffer = [], ""
    for line in advanced_text.splitlines():
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            if buffer.strip(): statements.append(buffer)
            buffer = ""
    if buffer.strip(): raise SystemExit("Advanced SQL has an incomplete final statement")
    if len(statements) != 3: raise SystemExit(f"Expected three advanced SQL statements, got {len(statements)}")
    for query, filename in ((statements[1], "sql_resistance_rank.csv"), (statements[2], "sql_coverage_audit.csv")):
        cursor = conn.execute(query)
        output_rows = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        write_csv(args.output_dir / filename, list(output_rows[0]) if output_rows else [col[0] for col in cursor.description], output_rows)
    write_svg(args.output_dir / "sql_amr_summary.svg", summary_rows)
    manifest = {"pipeline": "AMR CSV ETL", "status": "SUCCESS", "input_filename": args.input.relative_to(ROOT).as_posix(),
                "input_sha256": hashlib.sha256(raw_bytes).hexdigest(), "rows_received": len(records), "rows_curated": inserted,
                "unique_isolates": len(organism_by_isolate), "organisms": sorted(set(organism_by_isolate.values())),
                "source_url": "NOT_APPLICABLE_SYNTHETIC_FIXTURE", "source_query": "Synthetic fixture bundled with this project",
                "retrieval_date": None, "run_utc": datetime.now(timezone.utc).isoformat(),
                "database_status": "SQLite in-memory; Python standard library",
                "data_provenance_note": "All input observations are synthetic and do not originate from patients, hospitals, or a biological surveillance source."}
    (args.output_dir / "provenance_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Loaded {inserted}/{len(records)} synthetic rows; exported {len(summary_rows)} SQL groups and {len(issues)} issue(s).")
    conn.close()


if __name__ == "__main__":
    main()
