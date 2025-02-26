import boto3
import os
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super().default(obj)

def getAndUpdateCount(db):
    """
    Get the visitor count from the databse if it exists, if it does not, create an entry
    in the database. If it does, update the value in the database. Return the created/updated value
    """
    return db.update_item(
            **{ "Key" : {"visitor-count-id": "1"},
                "UpdateExpression" : "SET #num = if_not_exists(#num, :zero) + :inc",
                "ExpressionAttributeNames" : {"#num": "visitor-count"},
                "ExpressionAttributeValues" : {
                    ":inc": 1,
                    ":zero": 0
                },
                "ReturnValues" : "UPDATED_NEW"
            }
        )["Attributes"]

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

    return {
            'statusCode': 200,
            'headers': {
                        "Access-Control-Allow-Headers" : "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET"
                        },
            'body': json.dumps(getAndUpdateCount(dynamo, cls=DecimalEncoder)),
            'isBase64Encoded': False
            }
