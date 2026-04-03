import json
from decimal import Decimal

from flask import Flask, jsonify, request
from flask_cors import CORS

import boto3
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# --- App setup ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
devices_table = dynamodb.Table("Devices")
sns = boto3.client("sns", region_name="us-west-2")
secrets = boto3.client("secretsmanager")



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    token = data.get('token')
    phone_number = data.get('phoneNumber')

    if not token or not phone_number:
        return jsonify({"error": "Missing token or phoneNumber"}), 400


    try:

        devices_table.put_item(
            Item={
                "phoneNumber": phone_number,
                "token": token,
            }
        )

        return jsonify({
            "message": "Device registered successfully",
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/set_gps', methods=['POST'])
def set_gps():
    try:
        data = request.json
        phone_number = data.get('phoneNumber')
        lat = data.get('lat')
        lon = data.get('lon')

        if not phone_number:
            return {"error": "Missing phoneNumber"}, 400

        if lat is None or lon is None:
            return {"error": "Missing lat/lon"}, 400

        # Check if device exists
        response = devices_table.get_item(Key={"phoneNumber": phone_number})
        item = response.get("Item")

        if not item:
            return {"error": "Device not found"}, 404

        # Update GPS fields using Decimal
        devices_table.update_item(
            Key={"phoneNumber": phone_number},
            UpdateExpression="SET lastLat = :lat, lastLon = :lon",
            ExpressionAttributeValues={
                ":lat": Decimal(str(lat)),
                ":lon": Decimal(str(lon))
            }
        )

        return jsonify({
            "message": "GPS updated successfully",
            "phoneNumber": phone_number,
            "lat": lat,
            "lon": lon
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/get_gps', methods=['GET'])
def get_gps():
    try:
        phone_number = request.args.get("phoneNumber")

        if not phone_number:
            return {"error": "Missing phoneNumber"}, 400

        response = devices_table.get_item(Key={"phoneNumber": phone_number})
        item = response.get("Item")

        if not item:
            return jsonify({"error": "Device not found"}), 404

        # Convert Decimal → float for JSON
        lat = float(item.get("lastLat"))
        lon = float(item.get("lastLon"))


        return jsonify({
            "phoneNumber": phone_number,
            "lat": lat,
            "lon": lon,

        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/gps', methods=['POST'])
def gps():
    data = request.json
    phone_number = data.get('phoneNumber')

    if not phone_number:
        return {"error": "Missing phoneNumber"}, 400

    response = devices_table.get_item(Key={"phoneNumber": phone_number})
    item = response.get("Item")

    if not item:
        return {"error": "Device not found"}, 404

    fcm_token = item["token"]

    secret_value = secrets.get_secret_value(SecretId='firebase-service-account')
    service_account_info = json.loads(secret_value['SecretString'])


    # Create credentials
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )

    try:
        credentials.refresh(Request())
    except Exception as e:
        print("REFRESH ERROR:", e)

    project_id = service_account_info["project_id"]

    # FCM v1 endpoint
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    # FCM message
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

    # Send push notification
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "FCM error", "details": response.text}), 500

    return jsonify({"message": "GPS request sent", "fcmToken": fcm_token}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)