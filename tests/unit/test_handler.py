from moto import mock_aws
from boto3 import resource
from visitor_count.VisitorCount import create, read, update
from .. import key, item, updated_item

@mock_aws
def createDB():
    dynamodb = resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName = "visitor-count",
        KeySchema=[{"AttributeName": "visitor-count-id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "visitor-count-id", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )
    return dynamodb.Table("visitor-count")

@mock_aws
def testRead():
    db = createDB()
    """
    Test if reading from database fails when item that does not exist is read
    """
    assert int(read(db, key)["ResponseMetadata"]["HTTPStatusCode"]) == 200

@mock_aws
def testCreate():
    db = createDB()
    create(db, item)
    assert int(read(db, key)["Item"]["number"]) == 0

@mock_aws
def testUpdate():
    db = createDB()
    create(db, item)
    update(db, updated_item)
    assert int(read(db, key)["Item"]["number"]) == 1
