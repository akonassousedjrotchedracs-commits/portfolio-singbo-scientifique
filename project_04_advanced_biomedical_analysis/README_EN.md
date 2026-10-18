# Project 04 — Biomedical Statistical Analysis

**Connection to the CV:** the CV lists biostatistics and statistical processing for the thesis. This is a separate demonstration using synthetic data, not a reanalysis of the 81 thesis patients.

## Objective and method

Calculate descriptive resistance proportions and 95% Wilson intervals after auditing fields, categories and duplicates. The published outputs cover six organism–antibiotic pairs, with two synthetic tests per pair.

## Results and limitations

For a proportion of 1/2, the 95% Wilson interval is approximately 9.45–90.55%. For 0/2, it ranges from 0 to about 65.76%. These wide intervals illustrate uncertainty with very small denominators; the data do not support clinical inference.

- [Detailed case page (French)](index.html)
- [Estimates and intervals](results/amr_estimates_with_wilson_ci.csv)
- [Quality audit](results/data_quality_audit.json)
- [Chart (SVG)](results/amr_wilson_intervals.svg)

[Version française](README.md)
