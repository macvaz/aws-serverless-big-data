CREATE EXTERNAL TABLE IF NOT EXISTS poc.cars_csv_submission_id_${submission_id} (
  `model` string,
  `mpg` double,
  `gear` integer
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://testddfv1/datasets/cars/submission_id_${submission_id}'
TBLPROPERTIES ('classification' = 'parquet');
