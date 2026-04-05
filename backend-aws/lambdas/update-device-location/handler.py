import json
import boto3
from urllib.parse import unquote

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Devices")

def lambda_handler(event, context):
    # Extract phone number from path
    raw_phone = event["pathParameters"]["phoneNumber"]
    phone_number = unquote(raw_phone).strip()

    if not phone_number:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing phone_number"})
        }

    # Fetch from DynamoDB
    result = table.get_item(Key={"phoneNumber": phone_number})
    item = result.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Device not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "latitude": float(item["latitude"]),
            "longitude": float(item["longitude"])
        })
    }
