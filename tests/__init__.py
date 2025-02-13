key = {"Key" : {"visitor-count-id" : "1"}}
item = {"Item": {"visitor-count-id": "1", "number": "0" }}
updated_item = {"Key": {"visitor-count-id": "1"},
                "UpdateExpression": "SET #num = :newNum",
                "ExpressionAttributeNames": {
                    "#num": "number"
                },
                "ExpressionAttributeValues": {
                    ":newNum": "1"
                }
            }