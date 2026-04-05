# websocketBroadcast Lambda (AWS)

This Lambda function listens to DynamoDB Stream events and sends real-time GPS updates to connected WebSocket clients using the API Gateway Management API. It is triggered whenever a record in the **Devices** table is modified.

## Purpose
- Detect changes to a device's GPS coordinates.
- Extract the WebSocket `connectionId` from the DynamoDB record.
- Push updated latitude/longitude to the connected client.

## How It Works
1. Lambda receives DynamoDB Stream records.
2. For each record with eventName `MODIFY`, it extracts:
   - `connectionId`
   - `latitude`
   - `longitude`
3. Builds a JSON message containing the updated coordinates.
4. Uses the API Gateway Management API to send the message to the WebSocket client.
5. Handles stale connections (GoneException).

## DynamoDB Requirements
The `Devices` table must contain:

- `phoneNumber` (primary key)
- `connectionId` (string)
- `latitude` (number)
- `longitude` (number)

These fields are updated by other Lambdas in the system.

## Environment Variables
- `APIGATEWAY_ENDPOINT` — The WebSocket API endpoint, e.g.:
  `https://abc123.execute-api.us-west-2.amazonaws.com/production`

## IAM Permissions
The Lambda requires:
- `dynamodb:DescribeStream`
- `dynamodb:GetRecords`
- `dynamodb:GetShardIterator`
- `execute-api:ManageConnections`

## Example Message Sent to Client
{
  "longitude": 34.78,
  "latitude": 32.07
}

