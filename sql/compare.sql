
	SELECT 			
							p.id,
							r.id,
                            r.added,
                            (
								SELECT 		rd.req_b_id
                                FROM 		requirements_distance rd
                                WHERE		rd.req_a_id = r.id
                                AND			rd.req_b_id IN
                                (
									SELECT			r_aux.id
                                    FROM 			requirements r_aux
                                    INNER JOIN	projects p_aux ON p_aux.code = r_aux.code
                                    WHERE			p_aux.domain = '/Finance/Investing'
                                    AND				p_aux.id <> p.id
                                    AND				r.added < r_aux.added
                                )
                                ORDER BY	r.added
                                LIMIT			1
                            ) req_b_id,
                            (
								SELECT 		rd.distance
                                FROM 		requirements_distance rd 
                                WHERE		rd.req_a_id = r.id
                                AND			rd.req_b_id IN
                                (
									SELECT			r_aux.id
                                    FROM 			requirements r_aux
                                    INNER JOIN	projects p_aux ON p_aux.code = r_aux.code
                                    WHERE			p_aux.domain = '/Finance/Investing'
                                    AND				p_aux.id <> p.id
                                    AND				r.added < r_aux.added
                                )
                                ORDER BY	r.added
                                LIMIT			1
                            ) distance
	FROM 			projects p
	INNER JOIN	requirements r ON p.code = r.code
	WHERE			p.domain = '/Finance/Investing'
	ORDER BY		r.added;