# Detailed methodology and results — SINGBO portfolio

## Scope and traceability

This document summarizes the methods described in the public project pages and the outputs included with the demonstration files. Working scripts are not part of this public repository. The demonstration fixtures are labelled `DEMO_SYNTHETIC`. They exercise the code, formats and output checks. Figures below are calculations on these inputs, not clinical prevalence estimates or real surveillance findings.

## Project 1 — Antimicrobial resistance

**Question.** How can descriptive summaries be calculated by organism and antibiotic while retaining S, I and R separately?

**Tools.** Python 3, pandas for CSV input, light cleaning and aggregation, Matplotlib for plotting, and CSV/JSON outputs.

**Executed steps.** Read CSV; check four required columns; convert required fields to strings and trim whitespace; uppercase result codes; validate S/I/R categories; stop on duplicate isolate-organism-antibiotic keys; calculate S/I/R counts and R proportion; export tables and plot.

**Results in the published CSV.** The synthetic dataset contains 100 observations across five organism–antibiotic pairs (20 tests per pair). *E. coli*–ceftriaxone: 6/20 (30%); *E. coli*–ciprofloxacin: 11/20 (55%); *K. pneumoniae*–ceftriaxone: 8/20 (40%); *K. pneumoniae*–ciprofloxacin: 4/20 (20%); *S. aureus*–cefoxitin: 7/20 (35%).

**Interpretation.** The script demonstrates aggregation and preservation of S/I/R. It cannot establish prevalence without a sampling design or harmonize undocumented breakpoint standards. Categories must match the original laboratory method and interpretive standard.

## Project 2 — Sequence quality control

**Tools.** Python 3, Biopython (`Bio.SeqIO`, `Bio.SeqUtils.gc_fraction`), pandas, FASTA, CSV and JSON.

**Executed steps.** Parse FASTA records; calculate sequence length and GC fraction; count ambiguous bases; scan the three forward-strand frames from ATG to TAA/TAG/TGA stop codons; export metrics.

**Fixture results.** seq01: 64 nt, 50% GC, no ambiguous bases, 12-nt candidate ORF. seq02: 63 nt, 49.21% GC, no ambiguous bases, no ORF detected. seq03: 64 nt, 42.86% GC, 8 ambiguous bases out of 64 (12.5%), no ORF detected.

**Interpretation.** QC identifies a sequence with a notable fraction of ambiguous symbols and checks metric generation. The ORF scan is intentionally simple; it is not annotation, does not scan the reverse strand and cannot identify taxonomy or infer resistance.

## Project 3 — SQL and ETL

**Tools.** Python 3, pandas, SQL, SQLite in the verified run, JSON manifest and SHA-256 input fingerprint.

**Executed steps.** Read normalized CSV; validate schema; trim and uppercase categories; check required values, S/I/R categories and duplicates; compute SHA-256; generate curated data, quality log, provenance manifest and SQL summaries.

**Fixture results.** The synthetic CSV used by ETL contains 191 synthetic rows, 191 generated identifiers and 2 species. The run completed with `SUCCESS` and generated SQL aggregates, window-function ranks, a coverage audit and reports. Queries can be reproduced from the supplied input.

**Interpretation.** A hash identifies the file used in a run but does not certify biological provenance. SQLite was the tested engine; migration to PostgreSQL, MySQL or DuckDB would require adaptation and a new test run. A DuckDB dependency in `requirements.txt` does not mean the verified loader used DuckDB: the execution output states SQLite.

## Project 4 — Proportions and Wilson intervals

**Tools.** Python 3, pandas, Matplotlib, the Wilson formula implemented in the script, CSV and JSON.

**Method.** After schema validation and an audit of missing values, duplicates and invalid categories, the script calculates per group the number of results, resistant count, R proportion and 95% Wilson confidence interval (z=1.96). Outputs include an audit, isolate-antibiotic matrix, yearly summaries when a year field exists, a manifest and a figure.

**Example results.** One resistant result out of two gives 50%, with a 95% Wilson CI of approximately 9.45–90.55%. Zero resistant results out of two gives 0%, with an upper bound around 65.76%. These wide intervals reflect uncertainty with very small denominators.

**Interpretation.** Wilson intervals are appropriate for binomial proportions and behave better than a simple normal approximation for small n, but they do not correct selection bias, dependence between isolates or classification error. Time trends are comparable only when procedures and populations are sufficiently comparable.

## Public repository artefacts

The tables, figures and manifests linked from the project pages are the published artefacts. Working scripts are not included in this repository, so the results document the supplied examples and do not represent a rerun reproducible from this repository alone. The synthetic datasets are neither CHU-MEL data nor patient records.

## Checks required before analysing real data

1. Preserve the original source file as read-only and calculate its SHA-256.
2. Record URL, retrieval date, query, terms of use, data dictionary and S/I/R breakpoint version.
3. Document exclusions and reasons rather than silently dropping them.
4. Define the unit of analysis and check repeated isolates.
5. Confirm denominators represent tests actually performed.
6. Manually compare a sample of source rows with curated rows.
7. Rerun tests on real files and archive software versions.
