# Projet 06 — Survie de l’enfant et estimations publiques

Analyse descriptive de l’indicateur World Bank WDI `SH.DYN.MORT` pour le Bénin, le Togo, le Ghana, la Côte d’Ivoire et le Nigeria, de 1990 à 2024. Le fichier joint est un instantané obtenu via l’API WDI le 18 octobre 2026; la source indiquait une mise à jour au 8 octobre 2026. Les 175 valeurs sont des estimations nationales modélisées associées à UN IGME, et non des comptes individuels de décès.

Depuis ce dossier, reproduire les sorties avec Python standard :

```sh
python scripts/reproduce.py
```

La page du projet affiche le graphique, des valeurs de repère et les limites. Aucune analyse de causalité, comparaison de qualité des soins ou donnée de patient n’est présentée. Voir `data/provenance.json` pour la requête source et `data/under5_mortality_public.csv` pour l’instantané.
