SELECT			*
FROM 			projects;

SELECT			domain, COUNT(1) amount
FROM 			projects
GROUP BY		domain
ORDER BY		amount DESC;

SELECT			*
FROM 			requirements;

SELECT 			count(*)
FROM 			requirements_distance;

SELECT 			* 
FROM 			recommendations
ORDER BY		1 DESC;

SELECT 			distance, sample, steps, COUNT(1) amount
FROM 			recommendations r
GROUP BY 	distance, sample, steps;

SELECT			*
FROM 			evaluations;

SELECT			rec.distance, rec.sample, rec.steps,
						CASE
							WHEN e.is_assertive = 1 
                            THEN 'V' 
                            ELSE '' 
						END assertive, 
                        count(1) amount
FROM 			evaluations e
INNER JOIN	recommendations rec ON rec.id = e.recommendation_id
INNER	JOIN	projects p ON p.id = rec.project_id
WHERE			rec.type = 'REQUIREMENT'
AND				CAST(rec.distance AS DECIMAL(5,2)) = 0.30
GROUP BY		rec.distance, rec.sample, rec.steps, assertive;