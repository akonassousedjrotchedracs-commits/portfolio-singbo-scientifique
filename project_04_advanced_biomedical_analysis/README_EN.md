# Project 04 — Biomedical Statistical Analysis

**Scientific context:** this separate demonstration illustrates a biostatistical method. This is a separate demonstration using synthetic data, not a reanalysis of the 81 thesis patients.

## Objective and method

Calculate descriptive resistance proportions and 95% Wilson intervals after auditing fields, categories and duplicates. The published input contains 300 synthetic records across six organism–antibiotic pairs, with 50 records per pair. The R proportion uses all valid S, I and R records as its denominator; I is retained as a separate category and is not recoded.

## Results and limitations

The published estimates and intervals are recalculated from the input CSV by the reproduction script. They describe only the synthetic fixture; they do not support clinical inference or estimate resistance in a population.

- [Detailed case page (French)](index.html)
- [Estimates and intervals](results/amr_estimates_with_wilson_ci.csv)
- [Quality audit](results/data_quality_audit.json)
- [Chart (SVG)](results/amr_wilson_intervals.svg)

[Version française](README.md)
