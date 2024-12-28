import boto3
import time

from typing import Dict
from string import Template

CLIENT = boto3.client('athena')

RESULT_OUTPUT_LOCATION = "s3://testddfv1/queries/"
EXECUTION_IDS = []
EXECUTION_STATUS = []

# PUBLIC API
def execute_query_sync(file_name: str, event: Dict[str, str]) -> bool:
    query = _complete_query(file_name, event)
    execution_id = _start_query_execution(query)
    EXECUTION_IDS.append(execution_id)
    status =  _has_query_succeeded(execution_id)
    EXECUTION_STATUS.append(status)
    return status

def get_final_response():
    return {
        'execution-status': EXECUTION_STATUS,
        'execution-ids': EXECUTION_IDS,
        'statusCode': 200
        }

# PRIVATE API
def _complete_query(query_file: str, parameters: Dict[str, str]) -> str: 
    with open(query_file, 'r') as f:
        template = Template(f.read())
    
    return template.substitute(parameters)

def _start_query_execution(query: str):
    response = CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
    )

    return response["QueryExecutionId"]

def _has_query_succeeded(execution_id: str):
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

        time.sleep(1)

    return False

