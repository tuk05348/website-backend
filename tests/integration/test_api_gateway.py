import os
import json
import requests
import boto3
import pytest
from ...visitor_count.VisitorCount import DecimalEncoder
from .. import key, item, updated_item
"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "VisitorCountApi"]

        if not api_outputs:
            raise KeyError(f"VisitorCountAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_api_gateway(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.post(api_gateway_url, json.dumps({"operation": "read", "payload": key}))

        assert response.status_code == 200

    def test_put(self, api_gateway_url):
        """ Post test data to the database and check the response """
        response = requests.post(api_gateway_url, json.dumps({"operation": "create", "payload": item})) 
        check = response = requests.post(api_gateway_url, json.dumps({"operation": "read", "payload": key}))
        print(check)
        assert response.status_code == 200
        assert int(check.json()["Item"]["number"]) == 0

    def test_update(self, api_gateway_url):
        """ Update test data and check the response """
        response = requests.post(api_gateway_url, json.dumps({"operation": "update", "payload": updated_item})) 
        check = response = requests.post(api_gateway_url, json.dumps({"operation": "read", "payload": key}))
        print(check)
        assert response.status_code == 200
        assert int(check.json()["Item"]["number"]) == 1