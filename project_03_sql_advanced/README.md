# Projet 03 — Modélisation SQL et pipeline ETL

**Lien avec le parcours :** le CV mentionne Python et SQL pour la manipulation et l’analyse de données. Ce projet montre une démonstration reproductible sur des observations microbiologiques synthétiques ; il n’est pas présenté comme un outil utilisé au CHU-MEL.

## Objectif et méthode

Structurer des observations d’antibiogramme, contrôler les champs et catégories S/I/R, conserver les anomalies, tracer le fichier d’entrée et produire des agrégations SQL.

## Résumé de l’exécution publiée

Le manifeste indique une exécution `SUCCESS` sur 12 lignes synthétiques, représentant quatre identifiants d’isolats et deux organismes. Six lignes d’agrégation sont publiées. Les métadonnées de source et de date de récupération sont indiquées comme non spécifiées ; l’empreinte SHA-256 identifie le fichier exécuté mais ne valide pas son origine biologique.

## Résultats

- [Présentation détaillée](index.html)
- [Graphique du résumé SQL (SVG)](results/sql_amr_summary.svg)
- [Résumé SQL](results/sql_amr_summary.csv)
- [Anomalies de qualité](results/data_quality_issues.csv)
- [Manifeste de provenance](results/provenance_manifest.json)

[English version](README_EN.md)
