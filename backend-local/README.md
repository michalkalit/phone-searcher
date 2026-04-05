# Legacy Flask Backend (Deprecated)

This folder contains the original Python/Flask backend that powered the early version of the Device Tracking Demo System.  
It has since been **fully replaced by the AWS-based backend**, but is included here for reference and historical context.

The Flask server handled:
- Device registration
- GPS updates
- Fetching last known GPS
- Triggering FCM push notifications to request GPS from a device

Although deprecated, this code demonstrates the initial architecture before the migration to AWS Lambda, API Gateway, DynamoDB, and WebSocket APIs.

---


**API Endpoints**

### `POST /register`
Registers a device by storing:
- phone number  
- FCM token  

Data is saved in the `Devices` DynamoDB table.

---

### `POST /set_gps`
Updates a device’s last known GPS coordinates.

Payload:
json
{
  "phoneNumber": "+123456789",
  "lat": 32.07,
  "lon": 34.78
}


### `GET /get_gps?phoneNumber=...`
Returns the last known GPS coordinates for a device


### `POST /gps`
Triggers a push notification to the device via FCM v1 API.

The notification instructs the device to send back its GPS location
{
  "action": "get-gps",
  "phoneNumber": "..."
}
