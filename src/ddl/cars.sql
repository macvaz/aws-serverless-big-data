create database poc;

CREATE EXTERNAL TABLE IF NOT EXISTS `poc`.`cars` (
  `model` string,
  `mpg` double,
  `gear` integer
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://testddfv1/datasets/cars/'
TBLPROPERTIES ('classification' = 'parquet');
