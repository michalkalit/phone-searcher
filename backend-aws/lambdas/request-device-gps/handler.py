import json
import boto3
import requests
import urllib.parse
from google.oauth2 import service_account
from google.auth.transport.requests import Request

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Devices")
secrets = boto3.client("secretsmanager")


def lambda_handler(event, context):
    try:
        # Read phone number from path
        path_params = event.get("pathParameters") or {}
        raw_phone = path_params.get("phoneNumber", "")
        phone_number = urllib.parse.unquote(raw_phone)

        if not phone_number:
            return _response(400, {"error": "Missing phoneNumber"})

        # Lookup device in DynamoDB
        result = table.get_item(Key={"phoneNumber": phone_number})
        item = result.get("Item")

        if not item:
            return _response(404, {"error": "Device not found"})

        fcm_token = item["token"]

        # Load Firebase service account from Secrets Manager
        secret_value = secrets.get_secret_value(
            SecretId="firebase-service-account"
        )
        try:
            service_account_info = json.loads(secret_value["SecretString"])
            print("SECRET PARSED OK")
        except Exception as e:
            print("SECRET PARSE ERROR:", str(e))


        # Create Google credentials
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )

        credentials.refresh(Request())
        project_id = service_account_info["project_id"]

        # FCM endpoint
        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        payload = {
            "message": {
                "token": fcm_token,
                "data": {
                    "action": "get-gps",
                    "phoneNumber": phone_number
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return _response(500, {
                "error": "FCM error",
                "details": response.text
            })

        return _response(200, {
            "message": "GPS request sent",
            "fcmToken": fcm_token
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
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }
