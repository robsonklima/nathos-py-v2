
	SELECT 			req_a.description, req_b.description, d.distance
    FROM 			requirements_distance d
    INNER JOIN	requirements req_a ON req_a.id = d.req_a_id
    INNER JOIN	requirements req_b ON req_b.id = d.req_b_id
    ORDER BY		distance ASC;
    
    SELECT 			COUNT(1)
    FROM 			requirements_distance d
    INNER JOIN	requirements req_a ON req_a.id = d.req_a_id
    INNER JOIN	requirements req_b ON req_b.id = d.req_b_id
    ORDER BY		distance ASC;
    
    SELECT 			AVG(distance)
    FROM 			requirements_distance d;
    
    SELECT 			r.code, COUNT(1)
	FROM 			projects p
	INNER JOIN	requirements r ON r.code = p.code
	group by 			r.code
	ORDER BY		COUNT(1) DESC;

	SELECT			*
    FROM				projects;
    
    SELECT			domain, count(1) amount
    FROM				projects
    GROUP BY		domain
    ORDER BY 	amount DESC;

	SELECT 			* 
    FROM 			requirements;