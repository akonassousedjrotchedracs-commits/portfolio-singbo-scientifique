-- Educational queries over synthetic data; SQLite 3.25+ for window functions.
-- CTE: calculate group counts once, then present rates.
WITH counts AS (SELECT o.name organism,a.name antibiotic,COUNT(*) n,
 SUM(x.result='R') r,SUM(x.result='I') i,SUM(x.result='S') s
 FROM susceptibility_results x JOIN isolates USING(isolate_id)
 JOIN organisms o USING(organism_id) JOIN antibiotics a USING(antibiotic_id)
 GROUP BY o.name,a.name)
SELECT *,ROUND(100.0*r/NULLIF(n,0),1) resistant_pct FROM counts;

-- Window ranking retains tied proportions.
WITH rates AS (SELECT o.name organism,a.name antibiotic,COUNT(*) n,
 1.0*SUM(x.result='R')/COUNT(*) resistant_fraction
 FROM susceptibility_results x JOIN isolates USING(isolate_id)
 JOIN organisms o USING(organism_id) JOIN antibiotics a USING(antibiotic_id)
 GROUP BY o.name,a.name)
SELECT *,RANK() OVER(PARTITION BY organism ORDER BY resistant_fraction DESC) resistance_rank
FROM rates ORDER BY organism,resistance_rank,antibiotic;

-- Coverage audit shows missing organism-antibiotic combinations.
SELECT o.name organism,a.name antibiotic,COUNT(x.result_id) observed_n
FROM organisms o CROSS JOIN antibiotics a
LEFT JOIN isolates i ON i.organism_id=o.organism_id
LEFT JOIN susceptibility_results x ON x.isolate_id=i.isolate_id AND x.antibiotic_id=a.antibiotic_id
GROUP BY o.name,a.name ORDER BY o.name,a.name;
