# getLocation Lambda (AWS)

This Lambda function retrieves the last known GPS coordinates for a device stored in the **Devices** DynamoDB table. It is triggered by an API Gateway endpoint:

```
GET /devices/{phoneNumber}/location

```


## Purpose
- Accept a phone number from the API Gateway path parameters.
- Look up the device in DynamoDB.
- Return the stored latitude and longitude.


---

## How It Works
1. Extracts the `phoneNumber` from `event.pathParameters`.
2. URL‑decodes the phone number (important for `+` signs).
3. Queries DynamoDB using the phone number as the primary key.
4. If found, returns:
   ```json
   {
     "latitude": <float>,
     "longitude": <float>
   }
   ```
5. If not found, returns a 404 error.

---


## Example Successful Response
```json
{
  "latitude": 32.07,
  "longitude": 34.78
}

