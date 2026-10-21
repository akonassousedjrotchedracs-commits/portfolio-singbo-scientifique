# Rapport de tests et reproductibilité

## Scripts exécutés

Les quatre commandes ont été exécutées depuis la racine du dépôt avec Python installé dans l’environnement. Les fichiers ont été écrits dans `work/audit-run/` afin de préserver les sorties publiées.

| Projet | Commande exécutée | Résultat |
|---|---|---|
| 01 | `python project_01_antimicrobial_resistance/scripts/reproduce.py --output-dir work/audit-run/p01` | Réussi : 100 observations, 10 couples. |
| 02 FASTA | `python project_02_bacterial_sequence/scripts/reproduce.py --output-dir work/audit-run/p02` | Réussi : 3 séquences, 191 pb, 8 bases ambiguës. |
| 02 FASTQ | `python project_02_bacterial_sequence/scripts/reproduce_fastq_qc.py --output-dir work/audit-run/p02` | Réussi : 3 reads synthétiques, 60 bases, 20 cycles. |
| 03 | `python project_03_sql_advanced/scripts/run_pipeline.py --output-dir work/audit-run/p03` | Réussi : 191/191 lignes, 6 groupes, 0 anomalie. |
| 04 | `python project_04_advanced_biomedical_analysis/scripts/reproduce.py --output-dir work/audit-run/p04` | Réussi : 300 lignes auditées, 6 groupes. |

Tous les scripts s’appuient sur Python standard; SQLite est utilisé via le module intégré `sqlite3`. Aucun fichier `requirements.txt` n’est nécessaire pour ces commandes. Les rendus temporaires n’ont pas écrasé les résultats versionnés.

## Tests automatisés

`python -m unittest discover -s tests -v` — **6 tests réussis**.

- Projet 01 : contrôle des 100 observations et des dix couples de dix lignes.
- Projet 02 : cas FASTA ambigu accepté, séquence et en-tête dupliqués ou symboles invalides rejetés; FASTQ mal formé rejeté.
- Projet 03 : fixture distincte vérifiant la traçabilité d’une valeur manquante, d’une catégorie invalide et d’un doublon.
- Projet 04 : calcul de Wilson vérifié contre une valeur attendue, et contrôle du dénominateur de 300 lignes.
- HTML et Markdown : cibles locales, ancres HTML et images référencées vérifiées.

## Limites restantes

- La comparaison automatisée intégrale entre chaque tableau HTML et CSV n’est pas implémentée; les incohérences les plus visibles ont été vérifiées et corrigées au cours de l’audit.
- L’accueil et la page du mémoire ont été rendus avec Chrome headless en formats bureau et mobile. Le contrôle mobile révèle un débordement horizontal de contenu sur l’accueil qui reste à corriger; la page du mémoire s’affiche correctement. Le clavier et les contrastes n’ont pas fait l’objet d’un audit manuel complet. Le PDF a aussi été rendu et vérifié visuellement.
- Le document de soutenance a été contrôlé comme source des méthodes et agrégats rapportés. Aucun test statistique ne peut être reproduit sans les données individuelles ou tableaux sources; les valeurs rapportées n’ont pas été recalculées.
- La pièce confirme la filière Biotechnologie Médicale, la soutenance du 23 juillet 2024, l’effectif rapporté de 81 (61 rétrospectifs, 20 prospectifs), les périodes et les marqueurs PSA total/CRP/NFS. Elle n’indique pas la note de 17,67/20 et ne décrit aucun dosage de cytokines.
- Le PDF `portfolio_summary.pdf` a été reconstruit, extrait pour vérification du texte, rendu en trois pages puis inspecté visuellement. Les effectifs des projets sont synchronisés et les notes, mention et cytokines non étayées ont été retirées comme faits.
- Le script de génération est conservé dans `docs/audit/build_portfolio_summary.py` et s’exécute depuis la racine avec ReportLab installé : `python docs/audit/build_portfolio_summary.py`.
- Le workflow GitHub Pages n’a pas encore été déclenché; aucun push ou déploiement n’a eu lieu au moment de la rédaction de ce rapport.
