# Deep test plan — SINGBO portfolio

## Tests executed for this release

| Workflow | Input | Observed outcome |
|---|---|---|
| Project 1 — AMR analysis | `DEMO_SYNTHETIC_amr.csv` | Completed; CSV outputs and plot created |
| Project 2 — sequence QC | `DEMO_SYNTHETIC_sequences.fasta` | Completed; CSV/JSON report created |
| Project 3 — SQL queries | `DEMO_SYNTHETIC_amr_sql.csv` | Completed; database and summary created |
| Project 3 — ETL | `DEMO_SYNTHETIC_amr_sql.csv` | SUCCESS; 12 rows received/curated, 4 identifiers, 2 species |
| Project 4 — advanced analysis | `DEMO_SYNTHETIC_amr_sql.csv` | Completed; audit, estimates and plot created |

## Robustness tests to run after code changes

Test missing required columns, unknown result categories, duplicate isolate-antibiotic rows, missing required values, empty/unreadable FASTA, ambiguous bases, zero/all-resistant groups, empty inputs, SQL/Python aggregate agreement, SHA-256 changes after source modification and GitHub Pages relative links. These are recommended regression tests and are not claimed as all executed in this release. The five execution checks in the table were completed successfully.
