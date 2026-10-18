# Méthodologie et résultats détaillés — portfolio SINGBO

## Périmètre et principe de traçabilité

Ce document résume les méthodes décrites dans les fiches publiques et les résultats présents dans les fichiers de démonstration livrés. Les scripts de travail ne font pas partie de ce dépôt public. Les jeux de démonstration portent explicitement la mention `DEMO_SYNTHETIC`. Ils permettent d’exécuter le code, de contrôler les formats et de vérifier les sorties. Les chiffres ci-dessous sont donc des résultats de calcul sur ces entrées, pas des estimations de fréquence clinique ou de surveillance réelle.

## Projet 1 — Résistance aux antimicrobiens

**Question.** Comment calculer des résumés descriptifs par organisme et antibiotique tout en gardant séparées les catégories S, I et R ?

**Outils.** Python 3, pandas pour la lecture CSV, nettoyage léger et agrégation, Matplotlib pour le graphique, CSV/JSON pour les sorties.

**Étapes exécutées.** Lecture du CSV ; vérification des quatre champs obligatoires ; conversion des champs en chaînes et retrait des espaces ; passage des résultats en majuscules ; contrôle des catégories S/I/R ; arrêt si doublons dans la clé isolat-organisme-antibiotique ; calcul des nombres S/I/R et de la proportion R ; export des tableaux et de la figure.

**Résultats observés dans le CSV publié.** Le jeu contient 100 observations synthétiques, réparties sur cinq couples organisme–antibiotique (20 tests par couple). *E. coli*–ceftriaxone : 6/20 (30 %) ; *E. coli*–ciprofloxacine : 11/20 (55 %) ; *K. pneumoniae*–ceftriaxone : 8/20 (40 %) ; *K. pneumoniae*–ciprofloxacine : 4/20 (20 %) ; *S. aureus*–céfoxitine : 7/20 (35 %).

**Interprétation.** Le script démontre l’agrégation et le maintien de S/I/R. Il ne peut établir une prévalence sans plan d’échantillonnage, ni harmoniser des référentiels de seuils non documentés. Les catégories doivent correspondre au référentiel et à la méthode de laboratoire d’origine.

## Projet 2 — Contrôle qualité des séquences

**Outils.** Python 3, Biopython (`Bio.SeqIO`, `Bio.SeqUtils.gc_fraction`), pandas, FASTA, CSV et JSON.

**Étapes exécutées.** Lecture des enregistrements FASTA ; mesure de longueur ; calcul de la fraction GC ; décompte des bases ambiguës ; scan exploratoire des trois cadres sur le brin direct à partir d’ATG jusqu’à un codon stop TAA/TAG/TGA ; export des métriques.

**Résultats observés.** seq01 : 64 nt, GC 50 %, 0 base ambiguë, ORF candidat 12 nt. seq02 : 63 nt, GC 49,21 %, 0 base ambiguë, aucun ORF détecté. seq03 : 64 nt, GC 42,86 %, 8 bases ambiguës sur 64 (12,5 %), aucun ORF détecté.

**Interprétation.** Le contrôle repère une séquence contenant un taux notable de caractères ambigus et vérifie la génération des métriques. Le scan ORF est volontairement simple ; il n’est pas une annotation, ne cherche pas les ORF inversés et ne permet aucune identification taxonomique ou conclusion sur la résistance.

## Projet 3 — SQL et ETL

**Outils.** Python 3, pandas, SQL, SQLite dans l’exécution vérifiée, JSON pour le manifeste, SHA-256 pour l’empreinte du fichier source.

**Étapes exécutées.** Lecture de CSV normalisé ; contrôle de schéma ; normalisation des espaces et de la casse ; contrôle des valeurs obligatoires, catégories S/I/R et doublons ; calcul d’empreinte SHA-256 ; génération de données curées, journal de qualité, manifeste de provenance et résumés SQL.

**Résultats observés.** Le CSV synthétique utilisé par le pipeline ETL contient 12 lignes, 4 identifiants d’isolat et 2 espèces. L’exécution s’est terminée avec le statut `SUCCESS` et a généré la base et les rapports. Les requêtes sont reproductibles sur le fichier fourni.

**Interprétation.** L’empreinte permet de reconnaître le fichier utilisé lors d’une exécution, mais ne certifie pas sa provenance biologique. Le moteur testé est SQLite ; une migration vers PostgreSQL, MySQL ou DuckDB demanderait une adaptation et une nouvelle série de tests. La présence d’une dépendance DuckDB dans `requirements.txt` ne signifie pas que le chargeur vérifié a utilisé DuckDB : la sortie d’exécution indique SQLite.

## Projet 4 — Proportions et intervalles de Wilson

**Outils.** Python 3, pandas, Matplotlib, formule de Wilson implémentée dans le script, CSV/JSON.

**Méthode.** Après contrôle de schéma et audit des valeurs manquantes/doublons/catégories, le script calcule pour chaque groupe le nombre de résultats, le nombre R, la proportion R et l’intervalle de confiance à 95 % de Wilson (z=1,96). Les résultats comprennent un audit, une matrice isolat-antibiotique, des résumés annuels si l’année existe, un manifeste et une figure.

**Exemples de résultats.** Pour 1 R sur 2, la proportion est 50 % et l’IC Wilson à 95 % est approximativement 9,45–90,55 %. Pour 0 R sur 2, la proportion est 0 % et la borne supérieure est environ 65,76 %. La largeur de ces intervalles reflète l’incertitude élevée des très petits effectifs.

**Interprétation.** Les intervalles de Wilson sont adaptés à une proportion binomiale et se comportent mieux que l’approximation normale simple pour de petits n, mais ils ne corrigent ni biais de sélection, ni dépendance entre isolats, ni erreur de classification. Les tendances temporelles ne sont comparables que si les procédures et populations sont suffisamment comparables.

## Artefacts disponibles dans le dépôt public

Les tableaux CSV, figures et manifestes référencés dans les fiches sont les artefacts publiés. Les scripts de travail ne sont pas inclus dans ce dépôt ; les résultats documentent donc les exemples livrés et ne constituent pas une exécution reproductible à partir du dépôt seul. Les jeux synthétiques ne sont ni des données du CHU-MEL ni des données de patients.

## Contrôles à refaire avant toute analyse de données réelles

1. Conserver le fichier source original en lecture seule et calculer son SHA-256.
2. Noter l’URL, la date de téléchargement, la requête, les conditions d’utilisation, le dictionnaire de données et la version des seuils S/I/R.
3. Documenter les exclusions et leurs raisons, au lieu de les supprimer silencieusement.
4. Définir l’unité d’analyse et vérifier les isolats répétés.
5. Vérifier que les dénominateurs correspondent aux tests réellement effectués.
6. Comparer manuellement un échantillon de lignes source et de lignes curées.
7. Refaire les tests sur les fichiers réels et archiver les versions logicielles.
