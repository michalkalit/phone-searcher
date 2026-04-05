import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Devices")

def lambda_handler(event, context):
    try:
        connection_id = event["requestContext"]["connectionId"]
        params = event.get("queryStringParameters") or {}

        if "phoneNumber" not in params:
            return {"statusCode": 400, "body": "Missing phoneNumber"}

        phone = params["phoneNumber"]

        # Update the row
        table.update_item(
            Key={"phoneNumber": phone},
            UpdateExpression="SET connectionId = :c",
            ExpressionAttributeValues={":c": connection_id}
        )

        return {"statusCode": 200}

    except ClientError as e:
        print("DynamoDB error:", e)
        return {"statusCode": 500, "body": "Database error"}

    except Exception as e:
        print("Unexpected error:", e)
        return {"statusCode": 500, "body": "Internal server error"}
