import json
import boto3
from decimal import Decimal
import urllib.parse

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Devices")

def lambda_handler(event, context):
    try:
        path_params = event.get("pathParameters") or {}
        phone_number = path_params.get("encodedPhone")

        if not phone_number:
            return _response(400, {"error": "Missing phoneNumber in path"})

        # Decode URL-encoded phone number
        phone_number = urllib.parse.unquote(phone_number)


        # Parse JSON body
        body = event.get("body")
        if not body:
            return _response(400, {"error": "Missing request body"})

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return _response(400, {"error": "Invalid JSON body"})

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Validate required fields
        if latitude is None or longitude is None:
            return _response(400, {"error": "Missing latitude/longitude"})

        # Check if device exists
        result = table.get_item(Key={"phoneNumber": phone_number})
        item = result.get("Item")

        if not item:
            return _response(404, {"error": "Device not found"})

        # Update GPS fields
        table.update_item(
            Key={"phoneNumber": phone_number},
            UpdateExpression="SET latitude = :latitude, longitude = :longitude",
            ExpressionAttributeValues={
                ":latitude": Decimal(str(latitude)),
                ":longitude": Decimal(str(longitude))
            }
        )

        return _response(200, {
            "message": "GPS updated successfully",
            "phoneNumber": phone_number,
            "latitude": latitude,
            "longitude": longitude
        })

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,PUT,PATCH,POST"
        },
        "body": json.dumps(body)
    }
