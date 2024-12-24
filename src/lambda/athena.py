import awswrangler as wr

def lambda_handler(event, context):
   df = wr.athena.read_sql_query("SELECT * FROM cars", database="poc", ctas_approach=False)
   print(df.head())