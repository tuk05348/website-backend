import boto3
import os
import json

def getAndUpdateCount(db):
	response = db.get_item(Key={"visitor-count-id" : "1"})
	updated_count = 1
	if "Item" not in response:
		db.put_item(Item={"visitor-count-id": "1", "number": "1" })
	else:
		updated_count = int(response["Item"]["number"]) + 1
		db.update_item(Key={"visitor-count-id": "1"},
                UpdateExpression="SET #num = :newNum",
                ExpressionAttributeNames={"#num": "number"},
                ExpressionAttributeValues={
                    ":newNum": updated_count
                }
            )

	return {'visitor_count': updated_count}

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
            'body': json.dumps(getAndUpdateCount(dynamo)),
            'isBase64Encoded': False
            }
