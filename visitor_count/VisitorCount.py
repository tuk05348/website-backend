import boto3
import os
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

# Define some functions to perform the CRUD operations
def create(db, payload):
    return db.put_item(Item=payload['Item'])

def read(db, payload):
    return db.get_item(Key=payload['Key'])

def update(db, payload):
    return db.update_item(**{k: payload[k] for k in ['Key', 'UpdateExpression', 
    'ExpressionAttributeNames', 'ExpressionAttributeValues'] if k in payload})

operations = {
    'create': create,
    'read': read,
    'update': update
}

def lambda_handler(event, context):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
        operation being performed
    '''
    # Define the DynamoDB table that Lambda will connect to
    table_name = os.environ['DB_NAME']
    # Create the DynamoDB resource
    dynamo = boto3.resource('dynamodb').Table(table_name)

    event = json.loads(event['body'])
    operation = event['operation']
    payload = event['payload']

    if operation in operations:
        return {
                'statusCode': 200,
                'headers': {
                            "Access-Control-Allow-Headers" : "Content-Type",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "POST"
                            },
                'body': json.dumps(operations[operation](dynamo, payload), cls=DecimalEncoder),
                'isBase64Encoded': False
                }
    else:
        raise ValueError(f'Unrecognized operation "{operation}"')
