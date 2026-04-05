# registerDevice Lambda (AWS)

This Lambda function registers a device by storing its phone number and FCM token in the **Devices** DynamoDB table. It is triggered by an API Gateway endpoint:

POST /devices/register

## Purpose
- Accept a phone number and FCM token from the request body.
- Decode URL-encoded phone numbers.
- Store or update the device record in DynamoDB.

## How It Works
1. Parses the JSON body from the API Gateway event.
2. Extracts `phoneNumber` and `token`.
3. URL-decodes the phone number.
4. Writes the device record to DynamoDB using `put_item`.
5. Returns a JSON response confirming registration.

## DynamoDB Requirements
The `Devices` table must contain:

- `phoneNumber` (primary key)
- `token` (FCM device token)

## Example Request Body
{
  "phoneNumber": "+123456789",
  "token": "abcdef123456"
}

## Example Successful Response
{
  "message": "Device registered successfully"
}


