# Méthodologie et résultats détaillés — portfolio SINGBO

## Périmètre et principe de traçabilité

Ce document résume les méthodes décrites dans les fiches publiques et les résultats présents dans les fichiers de démonstration livrés. Les scripts sont inclus dans les cinq dossiers de projets et peuvent être exécutés avec Python standard. Les jeux des projets 01 à 04 sont synthétiques; leurs résultats ne sont pas des estimations de fréquence clinique ou de surveillance réelle.

## Projet 1 — Résistance aux antimicrobiens

**Question.** Comment calculer des résumés descriptifs par organisme et antibiotique tout en gardant séparées les catégories S, I et R ?

**Outils.** Python 3 standard (`csv`, `collections`, `pathlib`), CSV et SVG généré directement. Le script livré n’utilise pas pandas ni Matplotlib.

**Étapes exécutées.** Lecture du CSV ; vérification des quatre champs obligatoires ; conversion des champs en chaînes et retrait des espaces ; passage des résultats en majuscules ; contrôle des catégories S/I/R ; arrêt si doublons dans la clé isolat-organisme-antibiotique ; calcul des nombres S/I/R et de la proportion R ; export des tableaux et de la figure.

**Résultats observés dans le CSV publié.** Le jeu contient 100 observations synthétiques, réparties sur dix couples organisme–antibiotique (10 tests par couple). Les proportions R par groupe sont 20 %, 10 %, 30 %, 10 %, 40 %, 30 %, 40 %, 30 %, 20 % et 50 % (dans l’ordre du CSV de synthèse). Ce sont des résultats de calcul sur la fixture, pas des fréquences cliniques.

**Interprétation.** Le script démontre l’agrégation et le maintien de S/I/R. Il ne peut établir une prévalence sans plan d’échantillonnage, ni harmoniser des référentiels de seuils non documentés. Les catégories doivent correspondre au référentiel et à la méthode de laboratoire d’origine.

## Projet 2 — Contrôle qualité des séquences

**Outils.** Python 3 standard, FASTA, FASTQ, CSV, JSON et SVG. Les scripts n’importent ni Biopython ni pandas.

**Étapes exécutées.** Lecture des enregistrements FASTA ; mesure de longueur ; calcul de la fraction GC ; décompte des bases ambiguës ; scan exploratoire des trois cadres sur le brin direct à partir d’ATG jusqu’à un codon stop TAA/TAG/TGA ; export des métriques.

**Résultats observés.** seq01 : 64 nt, GC 50 %, 0 base ambiguë, ORF candidat 12 nt. seq02 : 63 nt, GC 49,21 %, 0 base ambiguë, aucun ORF détecté. seq03 : 64 nt, GC 42,86 %, 8 bases ambiguës sur 64 (12,5 %), aucun ORF détecté.

**Interprétation.** Le contrôle repère une séquence contenant un taux notable de caractères ambigus et vérifie la génération des métriques. Le scan ORF est volontairement simple ; il n’est pas une annotation, ne cherche pas les ORF inversés et ne permet aucune identification taxonomique ou conclusion sur la résistance.

## Projet 3 — SQL et ETL

**Outils.** Python 3 standard, `sqlite3`, SQL, JSON et SHA-256 pour l’empreinte du fichier source. Le script ne dépend pas de pandas.

**Étapes exécutées.** Lecture de CSV normalisé ; contrôle de schéma ; normalisation des espaces et de la casse ; contrôle des valeurs obligatoires, catégories S/I/R et doublons ; calcul d’empreinte SHA-256 ; génération de données curées, journal de qualité, manifeste de provenance et résumés SQL.

**Résultats observés.** Le CSV synthétique utilisé par le pipeline ETL contient 191 lignes synthétiques, 191 identifiants générés et 2 espèces. L’exécution s’est terminée avec le statut `SUCCESS` et a généré les agrégats SQL, le classement par fonction fenêtre, l’audit de couverture et les rapports. Les requêtes sont reproductibles sur le fichier fourni.

**Interprétation.** L’empreinte permet de reconnaître le fichier utilisé lors d’une exécution, mais ne certifie pas sa provenance biologique. Le moteur testé est SQLite ; une migration vers PostgreSQL, MySQL ou DuckDB demanderait une adaptation et une nouvelle série de tests. La présence d’une dépendance DuckDB dans `requirements.txt` ne signifie pas que le chargeur vérifié a utilisé DuckDB : la sortie d’exécution indique SQLite.

## Projet 4 — Proportions et intervalles de Wilson

**Outils.** Python 3 standard, formule de Wilson implémentée dans le script, CSV/JSON et SVG généré directement.

**Méthode.** Après contrôle de schéma, valeurs manquantes, catégories et doublons isolat–antibiotique, le script calcule pour chaque groupe le nombre de résultats valides S/I/R, le nombre R, R/n et l’intervalle de Wilson à 95 % (z=1,96). La catégorie I reste dans le dénominateur et demeure distincte; cette convention descriptive ne remplace pas le référentiel et la question scientifique applicables.

**Résultats.** Les six groupes contiennent chacun 50 lignes. Les proportions R sont respectivement 32 %, 48 %, 24 %, 60 %, 16 % et 40 %. Les bornes Wilson à 95 % sont calculées à la volée à partir des comptes R et n dans le script et sont exportées dans le CSV. Les résultats sont synthétiques et non cliniques.

**Interprétation.** Les intervalles de Wilson sont adaptés à une proportion binomiale et se comportent mieux que l’approximation normale simple pour de petits n, mais ils ne corrigent ni biais de sélection, ni dépendance entre isolats, ni erreur de classification. Les tendances temporelles ne sont comparables que si les procédures et populations sont suffisamment comparables.

## Artefacts disponibles dans le dépôt public

Les scripts, tableaux CSV, figures et manifestes référencés dans les fiches sont inclus dans le dépôt. Les quatre pipelines ont été exécutés pendant l’audit. Les jeux synthétiques ne sont ni des données du CHU-MEL ni des données de patients.

## Contrôles à refaire avant toute analyse de données réelles

1. Conserver le fichier source original en lecture seule et calculer son SHA-256.
2. Noter l’URL, la date de téléchargement, la requête, les conditions d’utilisation, le dictionnaire de données et la version des seuils S/I/R.
3. Documenter les exclusions et leurs raisons, au lieu de les supprimer silencieusement.
4. Définir l’unité d’analyse et vérifier les isolats répétés.
5. Vérifier que les dénominateurs correspondent aux tests réellement effectués.
6. Comparer manuellement un échantillon de lignes source et de lignes curées.
7. Refaire les tests sur les fichiers réels et archiver les versions logicielles.
