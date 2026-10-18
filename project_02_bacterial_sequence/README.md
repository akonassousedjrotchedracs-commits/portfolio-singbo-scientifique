# Projet 02 — Contrôle qualité de séquences bactériennes

Contrôle exploratoire de trois séquences FASTA synthétiques : longueur, fraction GC, bases ambiguës et recherche simple d’ORF sur le brin avant. Aucun résultat n’identifie un organisme ou n’annote un gène.

## Reproduire

Prérequis : Python 3, aucune dépendance externe. Depuis ce dossier :

```powershell
python scripts/reproduce.py
```

## Fichiers

- [Fiche détaillée](index.html)
- [Script Python](scripts/reproduce.py) · [entrée FASTA synthétique](data/DEMO_SYNTHETIC_sequences.fasta)
- [Résultats CSV](results/sequence_qc.csv) · [résumé JSON](results/sequence_qc_summary.json)
- [Graphique SVG](results/sequence_qc_overview.svg)

[English version](README_EN.md)


La page comporte aussi un exemple FASTQ distinct, entièrement synthétique, pour calculer des scores Phred+33/Q20/Q30 par lecture et par cycle. Il ne s’agit pas de données de séquençage réelles. Reproduction : `python scripts/reproduce_fastq_qc.py`.
