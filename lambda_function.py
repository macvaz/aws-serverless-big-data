import os

from lib.athena_wrapper import AthenaWrapper

# Memory footprint: 75 MBs. No extra layers required. Ends in 1 seconds
# Way faster than AwsWrangler
# NodeJS has a way clearer SDK for calling async APIs

def lambda_handler(event, context):
    # Create required DDL for csv file
    client =  AthenaWrapper(os.environ['QUERY_RESULT_LOCATION'])
    query_status = client.execute_query_sync("sql/ddl/car_table.sql", event, 0.1)

    # Apply DML logic to input data
    query_status = client.execute_query_sync("sql/dml/get_cars_by_brand.sql", event, 60)

    return client.get_final_response()