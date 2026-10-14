# Spécification de tableau de bord — Power BI / Data Analyst

## Objectif
Présenter de façon claire et contrôlée les observations d’antibiogrammes disponibles, sans assimiler les données manquantes à une sensibilité et sans transformer une base de surveillance en estimation de prévalence locale.

## Modèle de données recommandé
- `Isolates`: isolate_id, organism, collection_year, country, isolation_source, source_accession.
- `Susceptibility`: isolate_id, antibiotic, result, test_method, breakpoint_standard, breakpoint_version, test_date (si disponible).
- Relation : `Isolates[isolate_id]` 1 → * `Susceptibility[isolate_id]`. Une ligne de Susceptibility représente un test d’un antibiotique sur un isolat.
- Garder le CSV source intact et utiliser une table de correspondance pour normaliser les noms; ne jamais écraser les valeurs d’origine.

## Indicateurs
- Nombre d’isolats uniques (distinct count).
- Nombre d’observations AST (nombre de lignes).
- Nombre de tests R, I et S.
- Pourcentage R = R / (R + I + S) pour les tests classés, avec dénominateur visible.
- Part des données manquantes et taux de doublons.
- Nombre d’organismes, d’antibiotiques et de pays renseignés.
- Si les données sont adaptées : intervalles de confiance, par organisme et antibiotique.

## Visuels
1. Cartes KPI : isolats, tests, taux de complétude, doublons à résoudre.
2. Barres empilées 100 % S/I/R par organisme et antibiotique, avec le n affiché.
3. Matrice organisme × antibiotique avec %R et effectif testé.
4. Courbe temporelle uniquement si l’année de collecte est réellement disponible et suffisamment comparable.
5. Page qualité : données manquantes, catégories inconnues, doublons, provenance.

## Filtres
Organisme, antibiotique, année, pays, source d’isolement et standard de test, selon disponibilité.

## Règles à afficher dans le rapport
- « Un antibiotique non testé n’est pas une réponse sensible. »
- « Les proportions décrivent les enregistrements inclus; elles ne sont pas automatiquement représentatives d’une population. »
- Ne pas comparer directement les résultats issus de méthodes ou versions de breakpoints différentes sans harmonisation documentée.
- La résistance génotypique ne remplace pas le phénotype AST.

## État
Cette spécification est prête à servir de plan de construction dans Power BI. Aucun fichier `.pbix` n’est fourni dans cette livraison; les données de démonstration sont synthétiques.
