# Detailed methodology and results — SINGBO portfolio

## Scope and traceability

This document summarizes the methods and outputs included in the public project folders. Reproduction scripts are included and use the Python standard library. Projects 01–04 use synthetic fixtures; their results are not clinical prevalence estimates or surveillance findings.

## Project 1 — Antimicrobial resistance

**Question.** How can descriptive summaries be calculated by organism and antibiotic while retaining S, I and R separately?

**Tools.** Python 3 standard library (`csv`, `collections`, `pathlib`), CSV and directly generated SVG. The delivered script does not use pandas or Matplotlib.

**Executed steps.** Read CSV; check four required columns; convert required fields to strings and trim whitespace; uppercase result codes; validate S/I/R categories; stop on duplicate isolate-organism-antibiotic keys; calculate S/I/R counts and R proportion; export tables and plot.

**Results in the published CSV.** The synthetic dataset contains 100 observations across ten organism–antibiotic pairs (10 tests per pair). R proportions in summary order are 20%, 10%, 30%, 10%, 40%, 30%, 40%, 30%, 20% and 50%. These are calculations on the fixture, not clinical frequencies.

**Interpretation.** The script demonstrates aggregation and preservation of S/I/R. It cannot establish prevalence without a sampling design or harmonize undocumented breakpoint standards. Categories must match the original laboratory method and interpretive standard.

## Project 2 — Sequence quality control

**Tools.** Python 3 standard library, FASTA, FASTQ, CSV, JSON and SVG. The delivered scripts do not import Biopython or pandas.

**Executed steps.** Parse FASTA records; calculate sequence length and GC fraction; count ambiguous bases; scan the three forward-strand frames from ATG to TAA/TAG/TGA stop codons; export metrics.

**Fixture results.** seq01: 64 nt, 50% GC, no ambiguous bases, 12-nt candidate ORF. seq02: 63 nt, 49.21% GC, no ambiguous bases, no ORF detected. seq03: 64 nt, 42.86% GC, 8 ambiguous bases out of 64 (12.5%), no ORF detected.

**Interpretation.** QC identifies a sequence with a notable fraction of ambiguous symbols and checks metric generation. The ORF scan is intentionally simple; it is not annotation, does not scan the reverse strand and cannot identify taxonomy or infer resistance.

## Project 3 — SQL and ETL

**Tools.** Python 3 standard library, `sqlite3`, SQL, JSON and SHA-256 input fingerprint. The script does not depend on pandas.

**Executed steps.** Read normalized CSV; validate schema; trim and uppercase categories; check required values, S/I/R categories and duplicates; compute SHA-256; generate curated data, quality log, provenance manifest and SQL summaries.

**Fixture results.** The synthetic CSV used by ETL contains 191 synthetic rows, 191 generated identifiers and 2 species. The run completed with `SUCCESS` and generated SQL aggregates, window-function ranks, a coverage audit and reports. Queries can be reproduced from the supplied input.

**Interpretation.** A hash identifies the file used in a run but does not certify biological provenance. SQLite was the tested engine; migration to PostgreSQL, MySQL or DuckDB would require adaptation and a new test run. A DuckDB dependency in `requirements.txt` does not mean the verified loader used DuckDB: the execution output states SQLite.

## Project 4 — Proportions and Wilson intervals

**Tools.** Python standard library, the Wilson formula implemented in the script, CSV/JSON and directly generated SVG.

**Method.** After schema, missing-value, category and isolate–antibiotic duplicate checks, the script calculates valid S/I/R totals, R/n and a 95% Wilson interval (z=1.96) for each group. I stays in the denominator and remains a separate category; this descriptive convention does not replace the applicable interpretive standard or scientific question.

**Results.** Each of the six groups has 50 records. R proportions are 32%, 48%, 24%, 60%, 16% and 40%. The script computes the 95% Wilson bounds from R counts and denominators and exports them to CSV. Results are synthetic, not clinical.

**Interpretation.** Wilson intervals are appropriate for binomial proportions and behave better than a simple normal approximation for small n, but they do not correct selection bias, dependence between isolates or classification error. Time trends are comparable only when procedures and populations are sufficiently comparable.

## Public repository artefacts

The scripts, tables, figures and manifests linked from the project pages are included in this repository. The four pipelines were executed during this audit. Synthetic datasets are neither CHU-MEL data nor patient records.

## Checks required before analysing real data

1. Preserve the original source file as read-only and calculate its SHA-256.
2. Record URL, retrieval date, query, terms of use, data dictionary and S/I/R breakpoint version.
3. Document exclusions and reasons rather than silently dropping them.
4. Define the unit of analysis and check repeated isolates.
5. Confirm denominators represent tests actually performed.
6. Manually compare a sample of source rows with curated rows.
7. Rerun tests on real files and archive software versions.
