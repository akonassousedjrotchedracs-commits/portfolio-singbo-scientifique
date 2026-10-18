# Project 03 — SQL Modelling and ETL Pipeline

**Connection to the CV:** the CV lists Python and SQL for data manipulation and analysis. This is a reproducible demonstration on synthetic microbiological observations, not a tool reported as used at CHU-MEL.

## Objective and method

Structure susceptibility observations, validate fields and S/I/R categories, retain quality issues, fingerprint the input file and produce SQL aggregations.

## Published run summary

The manifest records `SUCCESS` for 12 synthetic rows, four isolate identifiers and two organisms. Six aggregation rows are published. Source metadata and retrieval date are unspecified; the SHA-256 fingerprint identifies the input file but does not validate its biological origin.

## Outputs

- [Detailed case page (French)](index.html)
- [SQL summary chart (SVG)](results/sql_amr_summary.svg)
- [SQL summary](results/sql_amr_summary.csv)
- [Quality issues](results/data_quality_issues.csv)
- [Provenance manifest](results/provenance_manifest.json)

[Version française](README.md)
