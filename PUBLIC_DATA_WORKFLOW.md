# Procédure de travail avec des données microbiologiques publiques

[English version](PUBLIC_DATA_WORKFLOW_EN.md)

## Objet
Ce protocole décrit comment préparer une analyse reproductible à partir d’un export public de données d’antibiogramme. Il ne signifie pas qu’un export NCBI est inclus dans ce dépôt : les données présentes sont des fichiers de démonstration.

## Procédure
1. Identifier la ressource publique et vérifier ses conditions d’utilisation et son dictionnaire de données.
2. Définir une question précise, les organismes, les antibiotiques, la période, la géographie et les critères d’inclusion.
3. Télécharger le fichier original sans le modifier ; noter l’URL, la date UTC, les filtres, la version et le SHA-256.
4. Examiner les champs d’identifiant, organisme, antibiotique, résultat, date/année, pays, accession, méthode et standard de seuils.
5. Créer une copie normalisée, conserver la source originale et documenter chaque correspondance de colonnes.
6. Définir l’unité d’analyse, repérer les isolats répétés et éviter de traiter des observations dépendantes comme indépendantes.
7. Contrôler les valeurs manquantes, les catégories S/I/R, les dénominateurs et la cohérence temporelle.
8. Exécuter les scripts, archiver les versions des logiciels et conserver les journaux de qualité.
9. Comparer un échantillon de lignes curées avec la source ; vérifier les totaux par une seconde méthode indépendante.
10. Présenter les résultats avec les effectifs, les dénominateurs, les incertitudes, les limites et la provenance exacte.

## Points d’attention
- Ne pas appeler un fichier « NCBI » sans accession ou métadonnées de provenance vérifiables.
- Ne pas mélanger les interprétations de seuils CLSI/EUCAST sans harmonisation documentée.
- Ne pas confondre proportion parmi les tests disponibles et prévalence dans une population.
- Ne jamais publier de données patient identifiantes ou des données hospitalières sans autorisation explicite et cadre approprié.
