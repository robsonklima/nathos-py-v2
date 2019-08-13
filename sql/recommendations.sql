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
                            THEN 'Y' 
                            ELSE 'N' 
						END assertive, 
                        count(1) amount
FROM 			evaluations e
INNER JOIN	recommendations rec ON rec.id = e.recommendation_id
INNER	JOIN	projects p ON p.id = rec.project_id
GROUP BY		rec.distance, rec.sample, rec.steps, e.is_assertive;