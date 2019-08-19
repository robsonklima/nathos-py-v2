SELECT 			*
FROM 			projects
ORDER BY		rand()
LIMIT 				24;

SELECT 			*
FROM 			risks;

SELECT 			code, count(1) amount
FROM 			risks
GROUP BY 	code
ORDER BY 	amount DESC;

SELECT 			*
FROM 			risks_distance;

SELECT 			p.*
FROM 			projects p
INNER JOIN	risks r ON r.code = p.code
GROUP BY		p.id;

SELECT			* 
FROM				recommendations
WHERE 			type='RISK';

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
WHERE			rec.type = 'RISK'
#AND				CAST(rec.distance AS DECIMAL(5,2)) = 0.30
GROUP BY		rec.distance, rec.sample, rec.steps, assertive;

SELECT			*
FROM				evaluations
ORDER BY 	1 DESC;

#DELETE FROM evaluations where added > '2019-08-19 08:54:41';
