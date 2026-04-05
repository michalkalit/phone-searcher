# updateLocation Lambda (AWS)

This Lambda function updates the GPS coordinates of a device stored in the **Devices** DynamoDB table. It is triggered by an API Gateway endpoint:

PUT /devices/{encodedPhone}/location

## Purpose
- Accept a phone number from the API Gateway path parameters.
- Decode URL-encoded phone numbers (e.g., %2B123 becomes +123).
- Parse the JSON body containing latitude and longitude.
- Update the device record in DynamoDB.

## How It Works
1. Extracts `encodedPhone` from `event.pathParameters`.
2. URL-decodes the phone number.
3. Parses the JSON body for `latitude` and `longitude`.
4. Validates that the device exists in DynamoDB.
5. Updates the `latitude` and `longitude` attributes using DynamoDB's UpdateExpression.
6. Returns a JSON response confirming the update.

## DynamoDB Schema
The Lambda expects the following attributes in the `Devices` table:

PK: phoneNumber (string)
latitude: number
longitude: number

## Environment Requirements
- IAM permissions:
  - dynamodb:GetItem
  - dynamodb:UpdateItem
- DynamoDB table named **Devices**
- API Gateway configured to pass `encodedPhone` as a path parameter

## Example Request Body
{
  "latitude": 32.07,
  "longitude": 34.78
}

## Example Successful Response
{
  "message": "GPS updated successfully",
  "phoneNumber": "+123456789",
  "latitude": 32.07,
  "longitude": 34.78
}

