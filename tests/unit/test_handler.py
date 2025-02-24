from pytest import fixture
from moto import mock_aws
from boto3 import resource
from visitor_count.VisitorCount import getAndUpdateCount

@fixture
def createDB():
	with mock_aws():
		dynamodb = resource("dynamodb", region_name="us-east-1")
		dynamodb.create_table(
        	TableName = "visitor-count",
        	KeySchema=[{"AttributeName": "visitor-count-id", "KeyType": "HASH"}],
        	AttributeDefinitions=[{"AttributeName": "visitor-count-id", "AttributeType": "S"}],
        	BillingMode='PAY_PER_REQUEST'
    	)
		yield dynamodb.Table("visitor-count")

@mock_aws
def testGetAndUpdateCount(createDB):
	"""
	Test if the lambda function returns the updated count from the database
	"""
	prev = getAndUpdateCount(createDB)
	cur = getAndUpdateCount(createDB)
	assert cur['visitor_count'] == (prev['visitor_count'] + 1)
