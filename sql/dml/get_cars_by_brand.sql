SELECT * 
FROM poc.cars_csv_submission_id_${submission_id}
WHERE model LIKE '%${car_brand}%'