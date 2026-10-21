# Audit complet du portfolio scientifique

## Périmètre et état initial

Audit du dépôt local `portfolio-singbo-scientifique`, branche `audit-portfolio-scientifique-20261021`, à partir d’un état initial propre (`main...origin/main`). Aucun changement antérieur n’a été trouvé. Aucun fichier n’a été poussé ni publié. Le document `TCHEDRAC CORRECTION AP SOUTENANCE.docx` fourni séparément a également été consulté; il n’a pas été copié dans le dépôt.

L’inventaire couvre les pages web, documents, profils, cinq projets, scripts, données, résultats, images et workflows. Aucun fichier `AGENTS.md` n’a été trouvé. Le workflow `.github/workflows/pages.yml` déploie le dépôt sur GitHub Pages lors d’un push sur `main` ou d’un déclenchement manuel. Aucun déploiement n’a été déclenché pendant cet audit. Toute publication ultérieure sur `main` déclenchera ce workflow.

## Inventaire

- Racine : `.gitignore`, `About`, `index.html`, `style.css`, `profile.html`, `profile-en.html`, `documentation.html`, `documentation-en.html`, `methodes-resultats.html`, `methods-results.html`, `README.md`, `README_EN.md`, `REFERENCES.md`, `portfolio_summary.pdf`.
- Documentation méthodologique : `DASHBOARD_POWERBI_SPEC_FR.md`, `DASHBOARD_POWERBI_SPEC_EN.md`, `EXPLANATORY_NOTES_FR.md`, `EXPLICATIONS_APPROFONDIES_FR.md`, `EXPLANATORY_NOTES_FR.md`, `EXPLANATIONS_DEEPENED_EN.md`, `METHODOLOGIE_ET_RESULTATS_FR.md`, `METHODOLOGY_AND_RESULTS_EN.md`, `PUBLIC_DATA_WORKFLOW.md`, `PUBLIC_DATA_WORKFLOW_EN.md`, `PUBLISH_ON_GITHUB_FR.md`, `TEST_PLAN_APPROFONDI_FR.md`, `TEST_PLAN_DEEP_EN.md`.
- Profil : `profile/PROFILE.md`, `profile/PROFILE_EN.md`; portrait : `assets/portrait-akonassou-singbo.jpg`.
- Projet 01 : `index.html`, deux README, `scripts/reproduce.py`, CSV source et trois CSV de résultats, cinq SVG pédagogiques/de résultats et deux PNG.
- Projet 02 : `index.html`, deux README, `scripts/reproduce.py`, `scripts/reproduce_fastq_qc.py`, fichiers FASTA/FASTQ synthétiques, CSV/JSON de résultats et quatre SVG.
- Projet 03 : `index.html`, deux README, CSV synthétique, `scripts/run_pipeline.py`, `sql/summary.sql`, `sql/advanced_queries.sql`, quatre CSV, manifeste JSON et trois SVG.
- Projet 04 : `index.html`, deux README, CSV synthétique, `scripts/reproduce.py`, CSV/JSON de résultats, deux SVG et un PNG.
- Projet 05 : `index.html`, deux README, figure PNG. Le document de soutenance fourni hors dépôt a été consulté; les tableaux sources et données individuelles ne figurent pas dans le dépôt ni dans le document fourni.

## Constats et gravité

| Gravité | Constat | Fichiers concernés | Action |
|---|---|---|---|
| Élevée | README du projet 01 annonçait cinq couples et 20 résultats par couple alors que source et script donnent 10 couples de 10. Le bloc « code complet » du HTML commençait par une copie HTML de la page. | `project_01_antimicrobial_resistance/README*.md`, `index.html`, `scripts/reproduce.py`, sorties | Harmoniser les effectifs, masquer le bloc parasite, conserver le véritable script et sa référence. |
| Élevée | Résumé du projet 04 en anglais annonçait deux observations par groupe, et des intervalles 1/2, en contradiction avec 300 lignes et n=50. | `project_04_advanced_biomedical_analysis/README_EN.md` | Corriger la définition et préciser le dénominateur S+I+R. |
| Élevée | `portfolio_summary.pdf` était obsolète par rapport aux sources : annonçait 5 couples au projet 01 au lieu de 10, 12 observations au projet 03 au lieu de 191, des intervalles pour n=2 au projet 04, des cytokines au mémoire et des notes/intitulés non vérifiés. | `portfolio_summary.pdf` | PDF reconstruit à partir des artefacts et du mémoire fourni; les éléments personnels non étayés ont été retirés ou explicitement qualifiés. |
| Élevée | Les pages du portfolio décrivaient le mémoire comme une simple synthèse et ne disposaient pas de la pièce source; un document de soutenance a depuis été fourni, mais pas les données individuelles. | Pages, README, documentation et document de soutenance fourni hors dépôt | Mettre à jour les faits vérifiés (filière, date, effectifs, marqueurs, méthodes déclarées) et garder les résultats agrégés explicitement rapportés, non recalculés. Le mémoire ne rapporte aucune mesure de cytokines. |
| Moyenne | Les méthodes transversales attribuent pandas, Biopython et Matplotlib à des projets dont les scripts livrés utilisent la bibliothèque standard. D’autres documents disent que les scripts ne sont pas fournis alors qu’ils sont présents. | `METHODOLOGIE_ET_RESULTATS_FR.md`, `METHODOLOGY_AND_RESULTS_EN.md`, notes | Corriger les outils et l’affirmation de reproductibilité après revue des scripts. |
| Moyenne | Projet 03 annonce un audit des anomalies, mais l’entrée principale est valide et l’audit initial est vide. | Projet 03, données et résultats | Documenter ce résultat et éprouver les rejets avec une fixture de test distincte. |
| Moyenne | Les parseurs ont des cas limites insuffisamment contrôlés (alphabet FASTA/FASTQ, reads vides, cohérence éventuelle de l’identifiant FASTQ). | Scripts du projet 02 | Revoir et tester explicitement ces entrées. |
| À confirmer | Le document confirme la filière Biotechnologie Médicale et une licence professionnelle visée, mais pas le diplôme délivré, le poste/date au CHU-MEL, ni la note/mention. | Accueil, profils, README, document de soutenance | Distinguer les éléments présents dans le mémoire des faits nécessitant une pièce officielle distincte. |
| Faible | La galerie est vide mais son statut « en préparation » est explicite. Le dépôt contient déjà des figures de projets, sans prétendre qu’elles forment une galerie personnelle. | `index.html`, ressources | Pas de correction nécessaire. |

## Résultats d’exécution initiale

- Projet 01 : 100 observations, 10 couples; le script a reconstruit les résumés dans un dossier temporaire.
- Projet 02 : FASTA, 3 séquences, 191 pb, 8 bases ambiguës; FASTQ, 3 reads, 60 bases, 20 cycles.
- Projet 03 : 191/191 lignes chargées, 6 groupes, zéro anomalie sur la fixture principale.
- Projet 04 : 300 lignes auditées, 6 groupes; les intervalles sont recalculés par le script.
- Les scripts ci-dessus s’exécutent avec Python standard; SQLite est le module Python intégré. Aucun recours à Biopython, pandas ou Matplotlib dans les scripts livrés.

Les vérifications et leurs limites figurent dans `RAPPORT_TESTS.md`. Les corrections et leurs résultats sont consignés dans `JOURNAL_DES_CORRECTIONS.md`. Aucun projet de recherche personnel, hypothèse de recherche ou protocole de recherche à réaliser n’a été ajouté.
