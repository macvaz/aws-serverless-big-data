from lib_athena_wrapper import execute_query_sync, get_final_response

# Memory footprint: 75 MBs. No extra layers required. Ends in 1 seconds
# Way faster!!
# NodeJS has a way clearer SDK for calling async APIs

def lambda_handler(event, context):
    # Create required DDL for csv file
    query_status = execute_query_sync("sql/ddl/car_table.sql", event)

    # Apply DML logic to input data
    query_status = execute_query_sync("sql/dml/get_cars_by_brand.sql", event)

    return get_final_response()