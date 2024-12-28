import awswrangler as wr

#Requires 256 MBs!! Slower to start up

def lambda_handler(event, context):
   df = wr.athena.read_sql_query("SELECT * FROM cars", database="poc", ctas_approach=False)
   print(df.head())