# websocketConnect Lambda (AWS)

This Lambda function handles WebSocket connection registration. It is triggered when a client connects to the WebSocket API and provides a phone number via query parameters. The Lambda stores the WebSocket `connectionId` in the **Devices** DynamoDB table so the backend can send real-time updates to the correct client.

## Purpose
- Extract the WebSocket `connectionId` from the API Gateway event.
- Read the `phoneNumber` from query string parameters.
- Store the `connectionId` in DynamoDB under the matching device record.

## How It Works
1. Reads `connectionId` from `event.requestContext.connectionId`.
2. Reads `phoneNumber` from `event.queryStringParameters`.
3. Updates the device record in DynamoDB using:
   ```
   UpdateExpression="SET connectionId = :c"
   ```
4. Returns HTTP 200 on success.
5. Logs and returns errors if DynamoDB or input validation fails.

## DynamoDB Requirements
The `Devices` table must contain:
- `phoneNumber` (primary key)
- `connectionId` (string, added by this Lambda)

## IAM Permissions
The Lambda requires:
- `dynamodb:UpdateItem`

## Example WebSocket Connect URL
wss://example.com/production?phoneNumber=%2B123456789

## Example Successful Response
```
{ "statusCode": 200 }
```


