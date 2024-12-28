import boto3
import time

from typing import Dict
from string import Template

class AthenaWrapper():
    def __init__(self, result_output_location: str):
        self.client = boto3.client('athena')
        self.result_output_location = result_output_location
        self.execution_ids = []
        self.execution_status = []
        
    # PUBLIC API
    def execute_query_sync(self, file_name: str, event: Dict[str, str]) -> bool:
        query = self._complete_query(file_name, event)
        execution_id = self._start_query_execution(query)
        self.execution_ids.append(execution_id)
        status =  self._has_query_succeeded(execution_id)
        self.execution_status.append(status)
        return status

    def get_final_response(self):
        return {
            'execution-status': self.execution_status,
            'execution-ids': self.execution_ids,
            'statusCode': 200
            }

    # PRIVATE API
    def _complete_query(self, query_file: str, parameters: Dict[str, str]) -> str: 
        with open(query_file, 'r') as f:
            template = Template(f.read())
        
        return template.substitute(parameters)

    def _start_query_execution(self, query: str):
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.result_output_location}
        )

        return response["QueryExecutionId"]

    def _has_query_succeeded(self, execution_id: str):
        state = "RUNNING"
        max_execution = 5

        while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
            max_execution -= 1
            response = self.client.get_query_execution(QueryExecutionId=execution_id)
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
