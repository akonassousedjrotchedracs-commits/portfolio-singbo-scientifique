# Workflow for public microbiology data

[Version française](PUBLIC_DATA_WORKFLOW.md)

This generic technical reference describes provenance safeguards for public antimicrobial-susceptibility exports. It is not a personal research project or announced work to be conducted. No NCBI export is included here; the available data are demonstration fixtures.

1. Identify the public resource and review its terms and data dictionary.
2. Define organisms, antibiotics, time period, geography and inclusion criteria.
3. Preserve the original download unchanged; record URL, UTC retrieval date, filters, version and SHA-256.
4. Inspect isolate ID, organism, antibiotic, result, year/date, country, accession, method and breakpoint standard.
5. Create a normalized copy, preserve the source and document every column mapping.
6. Define the unit of analysis, identify repeated isolates and avoid treating dependent observations as independent.
7. Check missing values, S/I/R categories, denominators and temporal consistency.
8. Run scripts, archive software versions and retain quality logs.
9. Compare a sample of curated rows against the source and independently cross-check totals.
10. Report counts, denominators, uncertainty, limitations and exact provenance.

Do not label a file as NCBI without verifiable provenance metadata. Do not mix CLSI/EUCAST interpretations without documented harmonization. A proportion among available tests is not necessarily population prevalence. Never publish identifiable patient or hospital data without authorization and an appropriate legal/ethical basis.
