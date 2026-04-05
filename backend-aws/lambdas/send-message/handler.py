import boto3
import json
import os

def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] not in ("MODIFY"):
            continue

        new_image = record["dynamodb"].get("NewImage", {})

        # Extract fields
        connection_id = new_image.get("connectionId", {}).get("S")
        longitude = new_image.get("longitude", {}).get("N")
        latitude = new_image.get("latitude", {}).get("N")

        if not connection_id:
            print("No connectionId found, skipping")
            continue

        # Build the message
        message = {
            "longitude": float(longitude) if longitude else None,
            "latitude": float(latitude) if latitude else None
        }       

        api = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=os.environ["APIGATEWAY_ENDPOINT"]
        )

        try:
            api.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(message).encode("utf-8")
            )
            print(f"Sent update to {connection_id}: {message}")

        except api.exceptions.GoneException:
            print(f"Connection {connection_id} is gone. Should delete from DB.")

        except Exception as e:
            print("Error sending message:", e)

    return {"statusCode": 200}
