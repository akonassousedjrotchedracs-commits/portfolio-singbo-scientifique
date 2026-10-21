# GUIDE EXPLICATIF APPROFONDI — PORTFOLIO SCIENTIFIQUE
## AKONASSOU SEDJRO TCHÉDRAC SINGBO
**Axes : microbiologie clinique, bioinformatique, Data Analytics, SQL et Data Engineering**

## 1. Objet et statut du travail
Ce dossier explique en détail les quatre projets du portfolio, les choix méthodologiques, les résultats produits, leur interprétation, les limites et les vérifications à effectuer. Il sert de support d’apprentissage et de préparation à une discussion avec un enseignant-chercheur.

**Statut des données :** les résultats chiffrés présentés dans cette édition proviennent de jeux de données synthétiques conçus pour tester les scripts. Ils ne sont pas issus du CHU-MEL, ne proviennent pas d’un patient et ne constituent pas une extraction de NCBI Pathogen Detection. Ils démontrent le fonctionnement des méthodes, pas une fréquence réelle de résistance ni une conclusion biologique. Cette distinction doit rester visible dans le PDF et le dépôt public.

**Statut de l’accès aux données publiques :** les sources officielles NCBI et le protocole d’extraction sont identifiés. Toutefois, l’environnement de construction n’a pas pu résoudre les noms de domaine externes lors de la tentative de téléchargement. Aucun export réel NCBI n’a donc été récupéré ici. Il serait incorrect d’affirmer que la validation empirique sur NCBI est achevée. La présente livraison documente intégralement les analyses exécutées sur les fichiers fournis et décrit la procédure de provenance à appliquer si un jeu de données public réel est ajouté à une édition ultérieure. Les résultats chiffrés de cette archive restent ceux des fichiers de démonstration.

## 2. Profil scientifique et fil conducteur
Le portfolio relie une formation en biotechnologie médicale et une expérience pratique de laboratoire hospitalier à des méthodes de traitement et d’analyse de données. Les domaines d’expérience comprennent notamment l’hématologie, la biochimie clinique, la sérologie, la microbiologie et la parasitologie. Le mémoire de licence porte sur les biomarqueurs inflammatoires dans les dysfonctionnements de la prostate, selon les informations communiquées. Ces expériences donnent un contexte scientifique à l’intérêt pour la qualité des mesures, la traçabilité et l’analyse biomédicale.

Le fil conducteur est le suivant :
1. comprendre comment un résultat de laboratoire est produit et documenté ;
2. vérifier la qualité et la structure de l’enregistrement ;
3. transformer des fichiers en tables fiables ;
4. calculer des indicateurs avec leurs dénominateurs ;
5. visualiser les résultats sans dépasser ce que les données permettent d’affirmer ;
6. documenter la provenance et permettre à un autre analyste de reproduire les étapes.

**Principe de présentation scientifique :** je présente ici les étapes que j’ai conçues, implémentées et exécutées, les contrôles effectués, les sorties obtenues et leur interprétation. Le contexte d’utilisation est décrit avec exactitude : je ne revendique pas une utilisation en routine hospitalière ou dans le mémoire si elle n’a pas eu lieu. Cette précision sur le contexte ne diminue pas ma contribution personnelle au travail technique et analytique.

## 3. Projet 1 — Analyse microbiologique de la résistance aux antimicrobiens
### 3.1 Question
Comment résumer proprement des résultats de sensibilité aux antibiotiques lorsque les données sont organisées en lignes isolat–antibiotique, tout en conservant la qualité des données et la signification du dénominateur ?

### 3.2 Structure attendue
Une ligne représente un résultat associé à un identifiant d’isolat, un organisme, un antibiotique et une catégorie d’interprétation. Les catégories prévues sont S, I et R. La signification exacte de ces catégories dépend du référentiel utilisé (par exemple EUCAST ou CLSI), de sa version, de l’espèce, de l’antibiotique et du contexte de test. Les catégories ne doivent pas être modifiées ou fusionnées sans justification.

### 3.3 Méthode
- Charger le fichier CSV sans écraser le fichier original.
- Contrôler la présence des colonnes obligatoires et la cohérence des types.
- Normaliser uniquement les variations de forme qui ne changent pas le sens (espaces superflus, casse si nécessaire), en journalisant la règle.
- Vérifier que la catégorie de résultat appartient au vocabulaire autorisé.
- Repérer les valeurs manquantes et les lignes répétées selon la clé métier pertinente. Une répétition isolat–antibiotique n’est pas automatiquement un doublon biologique : elle peut refléter plusieurs prélèvements, plusieurs dates ou plusieurs méthodes. La clé doit donc être adaptée aux métadonnées disponibles.
- Produire un décompte S/I/R par organisme et antibiotique.
- Calculer la proportion R comme R / nombre de tests interprétables pour cette combinaison, en explicitant si I est inclus ou exclu du dénominateur. Dans cette démonstration, le dénominateur est le nombre de résultats S+I+R enregistrés pour la combinaison ; la proportion R est R/(S+I+R).
- Exporter les données nettoyées, les résumés et un graphique.

### 3.4 Résultats de démonstration
Le CSV publié contient 100 observations synthétiques, réparties sur dix couples organisme–antibiotique, avec 10 tests par couple :
- **Escherichia coli — Ceftriaxone :** 6 résultats R sur 20, soit 30 % ;
- **Escherichia coli — Ciprofloxacin :** 11 résultats R sur 20, soit 55 % ;
- **Klebsiella pneumoniae — Ceftriaxone :** 8 résultats R sur 20, soit 40 % ;
- **Klebsiella pneumoniae — Ciprofloxacin :** 4 résultats R sur 20, soit 20 % ;
- **Staphylococcus aureus — Cefoxitin :** 7 résultats R sur 20, soit 35 %.

Ces valeurs sont des calculs sur un fichier artificiel. Elles ne doivent pas être interprétées comme une estimation de prévalence, une comparaison valable entre établissements ou une recommandation de traitement.

### 3.5 Interprétation correcte
Une proportion de résistance n’a de sens que si le nombre testé, la méthode, les critères d’interprétation, la période, l’origine des isolats et les éventuelles règles de déduplication sont compris. Par exemple, 1 résultat R sur 2 donne 50 %, mais l’incertitude est très importante. Il serait imprudent d’en déduire une tendance clinique ou de recommander un traitement.

### 3.6 Limites
- jeu synthétique et très petit ;
- aucune représentation de la diversité réelle des patients ou des établissements ;
- pas de référentiel clinique ou de version de breakpoint associé aux données artificielles ;
- absence de plan d’échantillonnage ;
- absence de correction de biais de sélection ;
- une ligne peut représenter un test et non un patient unique ;
- les catégories S/I/R ne sont comparables que si les règles d’interprétation sont harmonisées.

### 3.7 Évolutions scientifiques
Sur un jeu public réel, il faudra définir avant l’analyse la question, l’espèce, les dates, les pays ou régions si pertinents, les antibiotiques et les critères d’inclusion. Les résultats doivent présenter le numérateur et le dénominateur, les valeurs manquantes, les intervalles de confiance et une analyse de sensibilité aux règles de déduplication. Une analyse descriptive n’établit pas à elle seule une causalité.

## 4. Projet 2 — Contrôle qualité de séquences bactériennes
### 4.1 Question
Comment effectuer un contrôle initial de séquences nucléotidiques au format FASTA avant une analyse bioinformatique plus poussée ?

### 4.2 Étapes
1. Lire les enregistrements FASTA et conserver les identifiants originaux.
2. Mesurer la longueur de chaque séquence en paires de bases.
3. Calculer le pourcentage GC : (G+C)/nombre de bases A/C/G/T × 100, selon la convention explicitement appliquée.
4. Décompter les caractères ambigus ou non canoniques ; signaler que le pourcentage GC peut être biaisé si la proportion de bases ambiguës est élevée.
5. Calculer un candidat d’ORF simple sur le brin positif, uniquement comme indicateur exploratoire.
6. Écrire un tableau CSV et un résumé JSON afin de rendre les résultats exploitables en aval.

### 4.3 Résultats de démonstration
- **DEMO_SYNTHETIC_seq01|not_a_real_isolate :** longueur 64 pb ; GC 50.0 % ; bases ambiguës 0 (0.0 %) ; ORF simple maximal sur le brin positif : 12 nucléotides.
- **DEMO_SYNTHETIC_seq02|not_a_real_isolate :** longueur 63 pb ; GC 49.206 % ; bases ambiguës 0 (0.0 %) ; ORF simple maximal sur le brin positif : 0 nucléotides.
- **DEMO_SYNTHETIC_seq03|not_a_real_isolate :** longueur 64 pb ; GC 42.857 % ; bases ambiguës 8 (12.5 %) ; ORF simple maximal sur le brin positif : 0 nucléotides.

Le troisième enregistrement de démonstration contient des caractères ambigus ; le pipeline le signale. Ce résultat illustre l’utilité du contrôle qualité, mais ne signifie pas qu’une séquence bactérienne réelle est contaminée ou de mauvaise qualité.

### 4.4 Limites de l’approche ORF
La recherche simple d’ORF sur un seul brin n’est pas une annotation génomique. Une analyse robuste doit considérer les six cadres de lecture, le code génétique approprié, la longueur minimale, les codons de démarrage et d’arrêt, les pseudogènes, la qualité de l’assemblage et des outils d’annotation validés. Une séquence courte et artificielle ne permet aucune conclusion taxonomique ni fonctionnelle.

### 4.5 Portée de la démonstration
Pour des séquences publiques réelles, consigner l’accession, l’organisme indiqué par la source, la date de téléchargement, la version et la licence ou les conditions de réutilisation. Les identifications d’espèces ou les gènes de résistance doivent être confirmés avec les ressources appropriées et ne doivent pas être déduits uniquement du pourcentage GC.

## 5. Projet 3 — SQL et Data Engineering
### 5.1 Objectif
Construire une chaîne fiable allant d’un fichier brut à une base relationnelle analysable. Le projet met l’accent sur la reproductibilité, les contrôles de qualité, la traçabilité et la séparation des couches de données.

### 5.2 Architecture logique
- **Raw / source :** copie immuable du fichier fourni, accompagnée de sa provenance.
- **Staging :** données chargées sans interprétation clinique, avec contrôle de structure.
- **Validation :** tests de colonnes, valeurs autorisées, champs obligatoires, doublons potentiels et cohérence des identifiants.
- **Curated :** enregistrements retenus selon des règles documentées, avec journal des exclusions.
- **Analytical mart :** tables et vues destinées aux statistiques et au tableau de bord.
- **Exports :** CSV de résultats, base SQLite et manifeste JSON.

### 5.3 Pourquoi SQL ?
SQL permet de joindre des tables, regrouper des observations, calculer des indicateurs par groupe, filtrer des périodes et rendre explicites les règles de calcul. Les requêtes avancées utiles comprennent les jointures, CTE, agrégations conditionnelles, fonctions fenêtre et contrôles d’intégrité. SQLite est utilisé ici pour faciliter la portabilité ; le modèle peut être transposé à PostgreSQL ou DuckDB selon les besoins.

### 5.4 Contrôles importants
- unicité des identifiants techniques ;
- définition explicite de la clé métier ;
- valeurs S/I/R autorisées ;
- intégrité référentielle entre isolats, organismes, antibiotiques et résultats ;
- traçabilité des lignes exclues ;
- comptage avant et après chaque transformation ;
- vérification de cohérence entre SQL et les résultats Python ;
- conservation de la provenance, de la date et de l’empreinte du fichier source.

### 5.5 Limites
Un pipeline ETL ne garantit pas automatiquement la validité biologique des données. Il garantit seulement que les transformations programmées ont été appliquées de façon traçable. Les règles métier doivent être examinées par une personne compétente en microbiologie. Une base de données bien structurée peut contenir des données biaisées ou cliniquement mal interprétées.

## 6. Projet 4 — Data Analyst et biostatistiques avancées
### 6.1 Question
Comment passer de tableaux descriptifs à une analyse plus rigoureuse qui expose les dénominateurs, l’incertitude et la qualité des données ?

### 6.2 Contrôle qualité
Le rapport automatique de démonstration indique :
- lignes reçues : 12 ;
- doublons détectés selon la clé configurée : 0 ;
- résultats non valides : 0 ;
- champs manquants : aucun champ manquant dans cette fixture de démonstration, selon le rapport d’audit.

Ces constats portent uniquement sur le fichier synthétique et sur les règles programmées. L’absence d’erreur détectée n’équivaut pas à une preuve d’absence d’erreur dans la réalité.

### 6.3 Intervalles de confiance de Wilson
Pour une proportion observée p = x/n, l’intervalle de Wilson est une méthode adaptée aux proportions binomiales, notamment lorsque les effectifs sont petits ou lorsque la proportion est proche de 0 ou 1. L’intervalle donne une idée de l’incertitude d’échantillonnage sous les hypothèses du modèle. Il ne corrige pas les biais de sélection, la dépendance entre observations, les erreurs de classification ou la non-représentativité des données.

Exemples issus des données synthétiques :
- **Escherichia coli — Ceftriaxone :** 1 résistance(s) sur 2 test(s), proportion observée 50.0 %, IC à 95 % de Wilson [9.5 % ; 90.5 %].
- **Escherichia coli — Ciprofloxacin :** 1 résistance(s) sur 2 test(s), proportion observée 50.0 %, IC à 95 % de Wilson [9.5 % ; 90.5 %].
- **Escherichia coli — Gentamicin :** 0 résistance(s) sur 2 test(s), proportion observée 0.0 %, IC à 95 % de Wilson [0.0 % ; 65.8 %].
- **Klebsiella pneumoniae — Ceftriaxone :** 1 résistance(s) sur 2 test(s), proportion observée 50.0 %, IC à 95 % de Wilson [9.5 % ; 90.5 %].
- **Klebsiella pneumoniae — Ciprofloxacin :** 1 résistance(s) sur 2 test(s), proportion observée 50.0 %, IC à 95 % de Wilson [9.5 % ; 90.5 %].
- **Klebsiella pneumoniae — Gentamicin :** 1 résistance(s) sur 2 test(s), proportion observée 50.0 %, IC à 95 % de Wilson [9.5 % ; 90.5 %].

Les intervalles sont très larges parce que les effectifs sont très faibles. C’est un résultat pédagogique important : afficher uniquement un pourcentage pourrait donner une impression de précision qui n’existe pas.

### 6.4 Tendances temporelles et stratification
Une comparaison temporelle ne doit être réalisée que si les dates sont fiables, les définitions stables et les effectifs suffisants. Une hausse de proportion peut refléter un changement de composition des prélèvements, des pratiques de test ou de la population observée. Il faut montrer les effectifs par période, les données manquantes et, si nécessaire, stratifier par organisme, site ou autre variable pertinente.

### 6.5 Visualisation
Le tableau de bord recommandé comporte :
- cartes de synthèse : nombre d’isolats, nombre de tests, couverture des données ;
- barres de proportion R avec dénominateurs affichés ;
- matrice organisme–antibiotique ;
- évolution temporelle seulement si les métadonnées la permettent ;
- filtres pour période, organisme et pays/site si ces champs sont disponibles ;
- panneau de qualité des données et de provenance.

Les couleurs ne doivent pas être la seule information. Les graphiques doivent distinguer une valeur nulle d’une donnée absente et éviter les classements sur des effectifs trop faibles.

## 7. Portée et limites du portfolio
Cette documentation décrit les démonstrations techniques livrées et les limites des jeux de données synthétiques. Aucun export NCBI réel n’est inclus ou analysé dans cette version. Les sources mentionnées dans la bibliographie sont des références générales, et non l’annonce d’un projet de recherche ou d’une analyse à réaliser.

## 8. Validation logicielle
Les tests ne doivent pas seulement vérifier que le programme se lance. Ils doivent inclure :
- test du cas valide ;
- test d’un fichier vide ;
- test d’une colonne obligatoire absente ;
- test d’une catégorie S/I/R invalide ;
- test d’un résultat manquant ;
- test d’un doublon potentiel ;
- test d’un isolat avec plusieurs antibiotiques ;
- test d’un organisme avec aucun résultat R ;
- test de dénominateur nul ;
- test de séquence vide ;
- test de caractères ambigus dans FASTA ;
- test d’une séquence avec et sans codon stop ;
- test de cohérence des nombres de lignes avant/après ETL ;
- test de parité entre agrégations SQL et Python ;
- test de reproductibilité de la même entrée.

Chaque test doit comporter une entrée contrôlée, le résultat attendu, le résultat obtenu et le statut. Les données de test doivent être synthétiques et étiquetées comme telles.

## 9. Comment présenter le travail à un professeur
Une présentation honnête peut dire :
« Ce portfolio rassemble quatre projets indépendants réalisés pour appliquer des méthodes de programmation et d’analyse à des questions biomédicales. Les sorties actuellement fournies sont reproductibles sur des jeux de test synthétiques. J’ai documenté le pipeline et les limites, et je distingue explicitement cette démonstration d’une analyse de données publiques réelles. »

Après avoir réalisé toi-même les exécutions, les modifications et les lectures, tu pourras préciser ce que tu as personnellement implémenté, corrigé et appris. Ne revendique pas une compétence ou une conclusion que tu ne peux pas expliquer.

## 10. Références méthodologiques et techniques
- NCBI Pathogen Detection : https://www.ncbi.nlm.nih.gov/pathogens/
- NCBI Pathogen Detection Help : https://www.ncbi.nlm.nih.gov/pathogens/pathogens_help/
- NCBI AMR Resources / AST Browser : https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/resources/
- NCBI SRA : https://www.ncbi.nlm.nih.gov/sra
- NCBI Datasets : https://www.ncbi.nlm.nih.gov/datasets/
- Biopython documentation : https://biopython.org/wiki/Documentation
- Python documentation : https://docs.python.org/3/
- SQLite documentation : https://www.sqlite.org/docs.html
- EUCAST — clinical breakpoints and guidance: https://www.eucast.org/clinical_breakpoints/
- CLSI — standards and guidelines: https://clsi.org/standards/
- Wilson EB. Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association. 1927;22(158):209–212. doi:10.1080/01621459.1927.10502953

## 11. Conclusion générale
Le portfolio montre des démonstrations techniques reproductibles sur des données synthétiques et une synthèse prudente du mémoire à partir des éléments disponibles. Il distingue les calculs exécutés, les informations rapportées et les limites qui ne peuvent être vérifiées à partir du dépôt.
