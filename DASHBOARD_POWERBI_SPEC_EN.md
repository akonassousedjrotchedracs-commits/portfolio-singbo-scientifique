# Dashboard specification — Power BI / Data Analyst

## Purpose
Present antimicrobial-susceptibility observations clearly without treating missing tests as susceptible results or turning a surveillance database into a local prevalence estimate.

## Suggested data model
- `Isolates`: isolate_id, organism, collection_year, country, isolation_source, source_accession.
- `Susceptibility`: isolate_id, antibiotic, result, test_method, breakpoint_standard, breakpoint_version, test_date when available.
- Relationship: `Isolates[isolate_id]` 1-to-many `Susceptibility[isolate_id]`. Each susceptibility row represents one antibiotic test for one isolate.
- Preserve the source CSV and use a mapping table to normalize names; never overwrite original values.

## Indicators
- Unique isolate count (distinct count).
- Number of AST observations (row count).
- Number of R, I and S results.
- Resistance proportion by organism-antibiotic group, always displaying numerator and denominator.
- Distribution by year/country only when those fields are present and sufficiently comparable.

## Visuals and controls
- Bar chart of resistance proportion by organism and antibiotic, with denominator in tooltip.
- S/I/R stacked bars to preserve categories.
- Yearly line chart only when the period and test methods are comparable.
- Filters for organism, antibiotic, year and country.
- Data-quality page listing missing values, duplicates, unknown categories and source provenance.

## Interpretation rules
Do not interpret an untested antibiotic as susceptible. Do not compare categories across unharmonized breakpoint standards. Clearly label the unit of analysis and the data source. The current repository fixtures are demonstration data; a dashboard built from them is a technical demonstration, not a clinical surveillance report.

[Version française](DASHBOARD_POWERBI_SPEC_FR.md)
