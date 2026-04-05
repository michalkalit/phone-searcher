import json
import boto3
from urllib.parse import unquote

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Devices")

def lambda_handler(event, context):
    try:
        # Parse JSON body
        body = json.loads(event.get("body") or "{}")

        token = body.get("token")
        phone_number = body.get("phoneNumber")

        if not token or not phone_number:
            return _response(400, {"error": "Missing token or phoneNumber"})

        phone_number = unquote(phone_number).strip()

        # Write to DynamoDB
        table.put_item(
            Item={
                "phoneNumber": phone_number,
                "token": token
            }
        )

        return _response(200, {"message": "Device registered successfully"})

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
