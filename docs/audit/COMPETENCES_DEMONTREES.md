# Compétences démontrées par le dépôt

## Démontrées par un script ou un artefact reproductible

- Python standard : lecture/écriture CSV, JSON, validation élémentaire et génération SVG dans les projets 01, 02 et 04.
- Projet 01 : agrégation S/I/R, dénominateurs par couple et proportions R sur des observations synthétiques.
- Projet 02 : parsing FASTA, longueur, fraction GC, ambiguïtés, ORF exploratoire au brin avant; parsing FASTQ court, scores Phred+33, Q20/Q30 et indicateurs par cycle.
- Projet 03 : chargement CSV en SQLite en mémoire, contraintes relationnelles, agrégations SQL, requêtes de classement/couverture, rapport d’anomalies et empreinte SHA-256.
- Projet 04 : audit des valeurs et doublons, proportions R et intervalles de Wilson calculés depuis les données synthétiques.
- HTML/CSS : pages de présentation et ressources visuelles statiques.

## Partiellement démontrées

- Qualité des données : scripts de démonstration présents, mais certaines entrées pathologiques n’étaient pas vérifiées avant cet audit; consulter le rapport de tests.
- SQL avancé : requêtes SQLite sont livrées et exécutées par pipeline; la fixture principale ne contient aucune anomalie, d’où l’ajout d’une fixture de test séparée.
- Biostatistique : une formule de Wilson est codée et recalculée. Les données sont synthétiques; aucun test d’hypothèse ni inférence clinique n’est démontré par ce projet.
- Bioinformatique : exercices de parsing et de QC simples; pas d’assemblage, annotation, alignement, identification taxonomique ou analyse de variants.
- Power BI : une spécification de tableau de bord existe, mais aucun fichier `.pbix` ni tableau de bord opérationnel n’est fourni.

## Simplement mentionnées ou nécessitant des preuves supplémentaires

- Biopython, pandas et Matplotlib : mentionnés dans une documentation méthodologique, mais absents des scripts livrés. Leur utilisation n’est pas démontrée.
- Techniques et expérience hospitalières : elles sont décrites dans le profil, sans documents de preuve professionnelle dans ce dépôt; les projets synthétiques ne les valident pas.
- Intitulé de diplôme, poste exact, date d’entrée, distinctions, fonctions associatives, certifications et note académique : à confirmer par les sources originales.
- Mémoire de fin de formation : le document de soutenance a été fourni et vérifie le thème, la filière Biotechnologie Médicale, la date de soutenance, les effectifs et les méthodes déclarées. Les données individuelles et tableaux sources ne sont pas fournis; les résultats et analyses ne peuvent pas être recalculés indépendamment.

## Cadre d’interprétation

Les projets 01 à 04 sont des démonstrations sur des données synthétiques et ne constituent ni des résultats cliniques, ni de la surveillance hospitalière, ni une expérience sur des isolats réels. La catégorie I reste distincte et le projet 04 calcule R parmi les catégories S, I et R valides. Aucun seuil EUCAST/CLSI n’est appliqué aux fixtures.
