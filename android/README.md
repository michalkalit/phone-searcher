# Android Client

This is a minimal Android application used to demonstrate the mobile side of the Device Tracking Demo System. Its purpose is to show how a device can register with the backend, receive push notifications, and respond with GPS data.

This app is intentionally lightweight and exists to support the backend architecture — it is not a production mobile application.

## What the App Does
1. Registers the device by sending phone number and FCM token to the backend.
2. Listens for push notifications requesting GPS.
3. Generates a randomized GPS location and sends it back to the backend.
4. Handles runtime permissions.

## Code Structure
- MainActivity.kt: App startup, UI, registration flow
- FcmService.kt: Handles incoming FCM messages
- ApiClient.kt: OkHttp wrapper for backend calls
- DeviceInfo.kt: Retrieves phone number
- LocationSender.kt: Sends randomized GPS coordinates
- Permissions.kt: Runtime permission helpers

## Requirements
- Android 8.0+
- Firebase project configured
- google-services.json in the /app folder
- Backend URL configured in ApiClient.kt

## Running the App
1. Open the /android folder in Android Studio.
2. Add your google-services.json.
3. Update the backend URL if needed.
4. Run on a device or emulator.

## Notes
- GPS coordinates are randomized for demo purposes.
- The app is designed for backend testing, not end-users.
- This client was built to support the AWS backend workflow.
