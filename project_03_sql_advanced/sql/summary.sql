SELECT
    organisms.name AS organism,
    antibiotics.name AS antibiotic,
    COUNT(*) AS n_tested,
    SUM(CASE WHEN result = 'R' THEN 1 ELSE 0 END) AS resistant_n,
    SUM(CASE WHEN result = 'I' THEN 1 ELSE 0 END) AS intermediate_n,
    SUM(CASE WHEN result = 'S' THEN 1 ELSE 0 END) AS susceptible_n,
    ROUND(100.0 * SUM(CASE WHEN result = 'R' THEN 1 ELSE 0 END) / COUNT(*), 1) AS resistant_pct
FROM susceptibility_results
JOIN isolates USING (isolate_id)
JOIN organisms USING (organism_id)
JOIN antibiotics USING (antibiotic_id)
GROUP BY organisms.name, antibiotics.name
ORDER BY organisms.name, antibiotics.name;
