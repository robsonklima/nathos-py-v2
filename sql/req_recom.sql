SELECT 		distance, steps, sample, n_assertive, 
					CAST(n_assertive/total*100 AS DECIMAL(5,2)) n_asser_p, assertive, 
                    CAST(assertive/total*100 AS DECIMAL(5,2)) asser_p, total
FROM 
(
	SELECT 			distance, steps, sample,
							(
								SELECT 	COUNT(1) 
								FROM 	recommendations rb 
								WHERE 	CAST(r.distance AS DECIMAL(5,3)) = CAST(rb.distance AS DECIMAL(5,3))
								AND		CAST(r.steps AS DECIMAL(5,3)) = CAST(rb.steps AS DECIMAL(5,3))
								AND		CAST(r.sample AS DECIMAL(5,3)) = CAST(rb.sample AS DECIMAL(5,3))
								AND		rb.type = 'REQUIREMENT'
								AND		rb.is_assertive = 0
							) n_assertive,
							(
								SELECT 	COUNT(1) 
								FROM 	recommendations rb 
								WHERE 	CAST(r.distance AS DECIMAL(5,3)) = CAST(rb.distance AS DECIMAL(5,3))
								AND		CAST(r.steps AS DECIMAL(5,3)) = CAST(rb.steps AS DECIMAL(5,3))
								AND		CAST(r.sample AS DECIMAL(5,3)) = CAST(rb.sample AS DECIMAL(5,3))
								AND		rb.type = 'REQUIREMENT'
								AND		rb.is_assertive = 1
							) assertive,
							COUNT(1) total
	FROM 			recommendations r
	WHERE			r.type = 'REQUIREMENT'
	GROUP BY 	distance, sample, steps
) data
ORDER BY 	distance, steps, sample