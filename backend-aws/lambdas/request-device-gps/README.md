# requestGps Lambda (AWS)

This Lambda function sends a push notification to a device using Firebase Cloud Messaging (FCM). The notification instructs the device to send back its current GPS location. It is triggered by an API Gateway endpoint:

POST /devices/{phoneNumber}/gps

## Purpose
- Accept a phone number from the API Gateway path parameters.
- Look up the device in DynamoDB to retrieve its FCM token.
- Load Firebase service account credentials from AWS Secrets Manager.
- Generate an OAuth2 access token for the FCM v1 API.
- Send a push notification requesting GPS data.

## How It Works
1. Extracts `phoneNumber` from `event.pathParameters`.
2. URL-decodes the phone number.
3. Retrieves the device record from DynamoDB.
4. Loads the Firebase service account JSON from Secrets Manager.
5. Creates Google OAuth credentials and refreshes the access token.
6. Builds an FCM v1 API request with:
   - `action: get-gps`
   - the device's phone number
7. Sends the request to:
   https://fcm.googleapis.com/v1/projects/<project-id>/messages:send
8. Returns success or error details.

## DynamoDB Requirements
The `Devices` table must contain:

- `phoneNumber` (primary key)
- `token` (FCM device token)

## Secrets Manager Requirements
A secret named **firebase-service-account** must exist containing the full Firebase service account JSON.

## IAM Permissions
The Lambda requires:
- `dynamodb:GetItem`
- `secretsmanager:GetSecretValue`

## Example Successful Response
{
  "message": "GPS request sent",
  "fcmToken": "abcdef123456"
}


