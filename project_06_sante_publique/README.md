# Projet 06 · Santé publique au Bénin (2000–2024)

Analyse descriptive de quatre indicateurs publics (paludisme, mortalité des moins de 5 ans, couvertures DTC3 et rougeole) pour le Bénin, quatre pays voisins et l'Afrique subsaharienne. Données : API de la Banque mondiale (sources OMS, UNICEF, IGME).

## Reproduire

```bash
pip install matplotlib
python scripts/fetch_data.py   # télécharge data/indicateurs_bm.csv
python scripts/analyse.py      # écrit results/ (tableau et figures)
```

## Résultats principaux

- Couverture rougeole : 68 % en 2016, 44 % en 2024 (moyenne régionale stable, 69 %).
- Incidence du paludisme : 354 cas pour 1 000 personnes à risque en 2024, soit 1,55 fois la moyenne régionale.
- Mortalité des moins de 5 ans : 135 ‰ en 2000, 75 ‰ en 2024.

Analyse descriptive sur des estimations nationales ; aucune causalité n'est établie.
