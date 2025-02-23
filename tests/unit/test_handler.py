from pytest import fixture
from moto import mock_aws
from boto3 import resource
from visitor_count.VisitorCount import create, read, update
from .. import key, item, updated_item

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
def testRead(createDB):
    """
    Test if reading from database fails when item that does not exist is read
    """
    assert int(read(createDB, key)["ResponseMetadata"]["HTTPStatusCode"]) == 200

@mock_aws
def testCreate(createDB):
    create(createDB, item)
    assert int(read(createDB, key)["Item"]["number"]) == 0

@mock_aws
def testUpdate(createDB):
    create(createDB, item)
    update(createDB, updated_item)
    assert int(read(createDB, key)["Item"]["number"]) == 1
