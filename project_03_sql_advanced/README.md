# Projet 03 — Modélisation SQL et pipeline ETL

Pipeline reproductible pour valider des observations synthétiques S/I/R, charger un modèle relationnel SQLite en mémoire, conserver les anomalies et produire les agrégations avec SQL. Aucune source clinique n’est utilisée.

La fixture principale contient 191 lignes valides et ne produit aucune anomalie dans son journal. Une fixture de test séparée, `data/TEST_FIXTURE_with_anomalies.csv`, vérifie les rejets de champs manquants, de catégorie invalide et de doublon; elle n’est pas mélangée aux données principales.

## Reproduire

Prérequis : Python 3 (module SQLite inclus dans les distributions standard courantes), aucune dépendance Python externe. Depuis ce dossier :

```powershell
python scripts/run_pipeline.py
```

## Fichiers

- [Fiche détaillée](index.html)
- [Pipeline Python](scripts/run_pipeline.py) · [requête SQL](sql/summary.sql)
- [Données synthétiques](data/DEMO_SYNTHETIC_amr_sql.csv)
- [Résumé CSV](results/sql_amr_summary.csv) · [audit CSV](results/data_quality_issues.csv)
- [Manifeste](results/provenance_manifest.json) · [graphique SVG](results/sql_amr_summary.svg)

[English version](README_EN.md)
