# Notes explicatives du portfolio — version de travail pédagogique

**Auteur du portfolio : AKONASSOU SÈDJRO TCHÉDRAC SINGBO**

## 1. Pourquoi ces quatre axes ?

1. **Microbiologie clinique** : interpréter correctement les observations de laboratoire et garder les dénominateurs visibles.
2. **Bioinformatique** : vérifier et résumer des séquences biologiques avant toute interprétation.
3. **Data analyst** : nettoyer, explorer, résumer, quantifier l’incertitude, visualiser et expliquer les résultats.
4. **Data engineering / SQL** : transformer des fichiers en tables fiables, tester les contraintes, tracer les données et automatiser le flux.

Ce positionnement s’appuie sur mon parcours (Licence professionnelle en Biotechnologie médicale, laboratoire hospitalier) et sur des exercices Python/SQL reproductibles. Les scripts ne sont pas présentés comme ayant été utilisés au CHU-MEL.

## 2. Projet 1 — surveillance descriptive de la résistance aux antimicrobiens

### Question
Comment produire des tableaux de résistance à partir d’observations antibiogramme, sans confondre le nombre de tests avec le nombre d’isolats et sans supprimer la catégorie intermédiaire ?

### Méthodes
- Vérifier les champs obligatoires et les catégories S/I/R.
- Détecter les doublons par couple isolat–antibiotique.
- Calculer, pour chaque organisme et antibiotique, le nombre testé, R, I et S.
- Calculer une proportion descriptive R / nombre testé et un intervalle de confiance de Wilson à 95 %.
- Exporter les résultats, la matrice isolat–antibiotique et un manifeste de provenance.

### Interprétation prudente
La proportion n’est valable que pour les enregistrements présents et testés. Les isolats publics peuvent être sélectionnés, regroupés par flambée, concentrés dans certaines régions ou ne pas avoir tous les antibiogrammes. Les résultats ne représentent pas automatiquement la prévalence dans la population ni au Bénin. Un résultat génétique AMR n’est pas identique à un phénotype AST.

## 3. Projet 2 — contrôle qualité des séquences bactériennes

Le pipeline lit des fichiers FASTA, calcule la longueur, le pourcentage GC et les bases ambiguës, et repère des cadres de lecture ouverts candidats. Cette étape est exploratoire : elle ne remplace pas l’annotation génomique, l’identification taxonomique, le contrôle de contamination, ni une analyse de variants. Un ORF candidat n’est pas automatiquement un gène validé. Les fixtures fournies sont synthétiques.

## 4. Projet 3 — SQL et ingénierie des données

Le modèle sépare les observations de sensibilité (une ligne par isolat et antibiotique) des informations d’organisme et de contexte. L’ETL vérifie le schéma et les valeurs, conserve la provenance disponible, produit une empreinte SHA-256 et alimente l’exécution SQLite indiquée dans le manifeste publié. La démonstration n’est pas présentée comme un flux utilisé au CHU-MEL. Une empreinte identifie un fichier ; elle ne prouve ni son origine ni sa validité biologique.

### Pourquoi le SHA-256 ?
Il permet de vérifier que le fichier analysé est le même fichier source à travers les étapes. Il ne prouve ni que la source est vraie, ni que la donnée est correcte.

## 5. Projet 4 — data analyst / biostatistiques

Les résultats incluent audit qualité, résumé par organisme et antibiotique, intervalles de Wilson, matrice isolat–antibiotique et, si une année de collecte est présente, résumés descriptifs par année. Les valeurs manquantes restent manquantes : un antibiotique non testé n’est pas un résultat sensible. Les comparaisons temporelles ne sont interprétables que si la période, les méthodes, les populations et les règles de test sont suffisamment comparables.

### Pourquoi l’intervalle de Wilson ?
Pour une proportion binomiale, l’intervalle de Wilson se comporte généralement mieux que l’approximation normale simple, en particulier avec de petits effectifs ou des proportions proches de 0 ou 1. Cela ne corrige pas les biais de sélection ni les dépendances entre isolats.

## 6. Résultats de la démonstration fournie

Deux jeux de démonstration distincts sont publiés : le projet 01 contient 100 observations synthétiques sur dix couples organisme–antibiotique (10 par couple) ; le projet 03 contient 191 observations synthétiques, 191 identifiants générés et deux organismes. Leurs tableaux de résultats sont placés dans les dossiers `project_01_antimicrobial_resistance/results/` et `project_03_sql_advanced/results/`. Aucun des deux jeux ne constitue une découverte biologique ni un résultat hospitalier.

## 7. Données publiques : ce qui doit être vérifié

NCBI Pathogen Detection documente un navigateur d’isolats qui peut intégrer métadonnées, génotypes AMR et phénotypes AST. La disponibilité varie selon les enregistrements. Les résultats AST sont soumis par les contributeurs et NCBI précise qu’ils ne sont pas tous disponibles ni systématiquement validés au-delà de contrôles de base. Les analyses de fréquence exigent donc une prudence particulière.

Sources officielles :
- https://www.ncbi.nlm.nih.gov/pathogens/
- https://www.ncbi.nlm.nih.gov/pathogens/pathogens_help/
- https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/resources/
- https://www.ncbi.nlm.nih.gov/pathogens/ast
- https://www.ncbi.nlm.nih.gov/sra

**État des données dans cette livraison :** les fichiers locaux livrés ici sont des fixtures synthétiques. La documentation officielle NCBI a été consultée, mais aucun export CSV NCBI n’a pu être récupéré et exécuté dans l’environnement de construction (accès réseau sortant indisponible). En conséquence, ce dossier ne prétend pas avoir analysé des observations réelles NCBI. L’ETL accepte un export réel après téléchargement, mapping explicite des colonnes, vérification de provenance et relance.

## 8. Limites générales
- Le pipeline ne remplace pas un système de laboratoire accrédité ni la validation médicale.
- Les catégories S/I/R doivent suivre la norme et la version utilisées par la source (par exemple CLSI ou EUCAST) ; les règles ne doivent pas être mélangées sans harmonisation documentée.
- Les doublons sont détectés, mais leur résolution doit être justifiée à partir de la source.
- Les champs manquants, la représentativité et les différences de méthode peuvent biaiser les estimations.
- Le contrôle GC/longueur/ORF ne constitue pas une annotation complète.
- Un modèle prédictif ne doit pas être entraîné sur des données aussi petites sans validation indépendante, séparation adéquate des isolats et prévention de fuite de données.

## 9. Comment rendre le portfolio défendable
1. Lire ces notes et exécuter chaque commande.
2. Vérifier les résultats à la main sur quelques lignes.
3. Tenir un journal daté de ce que vous avez compris, modifié et appris.
4. Distinguer clairement les fixtures synthétiques de tout export public réel; aucune analyse NCBI n’est revendiquée dans cette livraison.
5. Avant toute publication ultérieure, contrôler le code, les rapports et l’absence de données patient ou d’identifiants confidentiels.
6. Dans les supports professionnels, ajouter le lien vers le dépôt GitHub public et, si souhaité, le lien vers le PDF du portfolio.
