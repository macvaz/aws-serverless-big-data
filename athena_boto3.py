import time
import boto3
import json

# Memory footprint: 75 MBs. No extra layers required. Ends in 1 seconds
# Way faster!!
# NodeJS has a way clearer SDK for calling async APIs

CLIENT = boto3.client('athena')
RESULT_OUTPUT_LOCATION = "s3://testddfv1/queries/"

def start_query_execution(query: str):
    response = CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
    )

    return response["QueryExecutionId"]

def get_query_results(execution_id: str):
    response = CLIENT.get_query_results(
        QueryExecutionId=execution_id
    )

    results = response['ResultSet']['Rows']
    return results

def has_query_succeeded(execution_id):
    state = "RUNNING"
    max_execution = 5

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = CLIENT.get_query_execution(QueryExecutionId=execution_id)
        if (
            "QueryExecution" in response
            and "Status" in response["QueryExecution"]
            and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                return True

        time.sleep(2)

    return False

def lambda_handler(event, context):
    named_query = CLIENT.get_named_query(NamedQueryId = "350dd0c3-322a-49e1-bd95-c88a947a40a5")
    execution_id = start_query_execution(named_query["NamedQuery"]["QueryString"])

    query_status = has_query_succeeded(execution_id)

    return {
        'statusCode': query_status,
        'body': json.dumps(get_query_results(execution_id=execution_id))
    }