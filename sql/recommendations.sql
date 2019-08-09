SELECT 		* 
FROM 			recommendations;

SELECT 			distance, sample, steps, COUNT(1) amount
FROM 			recommendations r
GROUP BY 	distance, sample, steps;