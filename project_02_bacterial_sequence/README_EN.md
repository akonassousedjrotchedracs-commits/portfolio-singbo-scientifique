# Project 02 — Bacterial Sequence Quality Control

**Positioning:** a complementary bioinformatics exercise in the portfolio. This is a technical exercise, not hospital experience or a clinical result.

## Objective and method

Calculate exploratory quality metrics for synthetic FASTA sequences: length, GC fraction, ambiguous bases and a simple forward-strand ORF indicator.

## Demonstration summary

The dataset contains three synthetic sequences totalling 191 bases, with eight ambiguous bases overall. These indicators are not bacterial identification, gene annotation or resistance analysis.

## Outputs

- [Detailed case page (French)](index.html)
- [Sequence QC chart (SVG)](results/sequence_qc_overview.svg)
- [Sequence QC table](results/sequence_qc.csv)
- [Summary JSON](results/sequence_qc_summary.json)

[Version française](README.md)


The page also contains a separate, fully synthetic FASTQ example for Phred+33/Q20/Q30 metrics by read and cycle. It is not real sequencer data. Reproduce with `python scripts/reproduce_fastq_qc.py`.
