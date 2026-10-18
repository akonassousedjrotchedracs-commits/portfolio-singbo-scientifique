# Projet 04 — Analyse statistique biomédicale

**Lien avec le parcours :** le CV mentionne la biostatistique et le traitement statistique du mémoire. Cette fiche est une démonstration séparée sur des données synthétiques, et non une nouvelle analyse des 81 patients du mémoire.

## Objectif et méthode

Calculer des proportions descriptives de résistance et leurs intervalles de Wilson à 95 %, après audit des champs, catégories et doublons. Les sorties couvrent six couples organisme–antibiotique, avec deux tests synthétiques par couple.

## Résultats et limites

Pour une proportion de 1/2, l’intervalle de Wilson à 95 % est d’environ 9,45–90,55 %. Pour 0/2, il s’étend de 0 à environ 65,76 %. Ces intervalles larges illustrent l’incertitude associée aux très petits effectifs ; les données ne soutiennent pas d’inférence clinique.

- [Présentation détaillée](index.html)
- [Estimations et intervalles](results/amr_estimates_with_wilson_ci.csv)
- [Audit qualité](results/data_quality_audit.json)
- [Graphique (SVG)](results/amr_wilson_intervals.svg)

[English version](README_EN.md)
