# Plan de tests approfondis — portfolio SINGBO

## Tests exécutés pour cette version

| Flux | Entrée | Résultat observé |
|---|---|---|
| Projet 1 — analyse AMR | `DEMO_SYNTHETIC_amr.csv` | Terminé sans erreur ; sorties CSV et graphique créées |
| Projet 2 — QC séquences | `DEMO_SYNTHETIC_sequences.fasta` | Terminé sans erreur ; rapport CSV/JSON créé |
| Projet 3 — requêtes SQL | `DEMO_SYNTHETIC_amr_sql.csv` | Terminé sans erreur ; base et résumé créés |
| Projet 3 — ETL | `DEMO_SYNTHETIC_amr_sql.csv` | Statut SUCCESS ; 12 lignes reçues/curées, 4 identifiants, 2 espèces |
| Projet 4 — analyse avancée | `DEMO_SYNTHETIC_amr_sql.csv` | Terminé sans erreur ; audit, estimations et figure créés |

## Tests de robustesse à effectuer si les scripts sont modifiés

1. Colonne obligatoire absente : l’exécution doit s’arrêter avec une erreur explicite.
2. Catégorie résultat non reconnue : l’exécution doit s’arrêter, sans recodage implicite.
3. Doublon isolat–antibiotique : le script concerné doit le signaler ou s’arrêter.
4. Valeur obligatoire manquante : vérifier la politique d’exclusion et quantifier l’exclusion.
5. FASTA vide ou fichier illisible : l’erreur doit être compréhensible.
6. Séquence avec N ou autres symboles ambigus : le rapport doit refléter ces caractères.
7. Groupe sans résultat R : proportion 0 % et intervalle cohérent si n > 0.
8. Groupe avec tous les résultats R : proportion 100 % et bornes dans [0,1].
9. Entrée vide ou dénominateur nul : aucune division par zéro ni résultat trompeur.
10. Comparer les agrégations SQL et Python sur les mêmes lignes.
11. Vérifier que le SHA-256 change si le contenu du fichier source change.
12. Vérifier les liens de `index.html` après publication GitHub Pages.

Ces cas de robustesse sont des tests à exécuter lors d’une évolution du code ; ils ne sont pas déclarés comme tous exécutés dans cette livraison. Les cinq tests d’exécution principaux du tableau, eux, ont été réalisés avec succès.
