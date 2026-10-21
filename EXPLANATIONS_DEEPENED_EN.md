# Detailed explanatory notes — English edition

This companion document explains the implemented portfolio methods and how to read the outputs. See [the French detailed guide](EXPLICATIONS_APPROFONDIES_FR.md) for the full extended walkthrough and [the detailed methodology/results report](METHODOLOGY_AND_RESULTS_EN.md) for exact output examples.

## How to read a project

1. Start with the research question and unit of analysis.
2. Inspect the input schema and data dictionary.
3. Read the script from input parsing through validation, transformation, analysis and export.
4. Compare output counts with the input rows and with the documented expected values.
5. Inspect figures together with denominators and the source data.
6. Separate software correctness from biological validity: a script can execute correctly on a fixture without producing evidence about a real population.

## Key methods

- **S/I/R summaries:** preserve the three categories and calculate resistance proportions within each organism-antibiotic group. Verify which records were actually tested and the applicable breakpoint standard.
- **Sequence QC:** length and GC fraction are descriptive; ambiguous bases are a warning signal. A simple forward-strand ORF scan is not gene annotation.
- **ETL and SQL:** schema validation, explicit normalization, duplicate checks, source hashing and provenance manifests support traceability. Hashes identify files; they do not prove the truth of their metadata.
- **Wilson confidence interval:** expresses binomial uncertainty around an observed proportion. With very small denominators, intervals are wide; confidence intervals do not correct sampling bias.

## Reproducibility

The public repository includes reproduction scripts, result tables, figures and manifests. Preserve the original input, document exclusions and compare transformed rows with the source before interpreting results.
