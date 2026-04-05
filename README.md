# Device Tracking Demo System

This project is a full end‑to‑end demo showing how a mobile device can send data through an AWS backend and update a live web client in real time.

It includes:
- A minimal Android client that registers with FCM and responds to backend commands
- An AWS backend (API Gateway, Lambda, DynamoDB, WebSocket API)
- A React web client that displays live device location updates

The goal of this project is to demonstrate architecture, event flow, and cloud integration — not to serve as a production mobile or web application.

---

**High‑Level Architecture**

          ANDROID DEVICE
   ┌──────────────────────────┐
   │  FCM Token + Phone       │
   │  Receives "get-gps"      │
   │  Sends GPS → Backend     │
   └──────────────┬──────────┘
                  │
                  ▼
        API GATEWAY (REST)
   ┌──────────────────────────┐
   │ /register                │
   │ /gps (send push)         │
   │ /location (update/get)   │
   └──────────────┬──────────┘
                  │
                  ▼
              LAMBDAS
   ┌──────────────────────────┐
   │ registerDevice           │
   │ requestGps (FCM)         │
   │ updateLocation           │
   │ getLocation              │
   └──────────────┬──────────┘
                  │
                  ▼
              DYNAMODB
   ┌──────────────────────────┐
   │ phoneNumber (PK)         │
   │ token                    │
   │ latitude / longitude     │
   │ connectionId             │
   └──────────────┬──────────┘
                  │ Stream
                  ▼
       websocketBroadcast Lambda
   ┌──────────────────────────┐
   │ Sends updates to client  │
   └──────────────┬──────────┘
                  │
                  ▼
        API GATEWAY (WEBSOCKET)
   ┌──────────────────────────┐
   │ Maintains connections    │
   └──────────────┬──────────┘
                  │
                  ▼
            REACT WEB CLIENT
   ┌──────────────────────────┐
   │ Receives GPS live        │
   │ Updates map instantly    │
   └──────────────────────────┘


---

**Flow Summary**
1. Android app registers with FCM and sends its token + phone number to the backend  
2. Backend stores device info in DynamoDB  
3. Backend can send a “get‑gps” push notification to the device  
4. Android responds by sending a (randomized) GPS location  
5. Backend writes the location to DynamoDB  
6. DynamoDB stream triggers a Lambda that pushes updates to connected WebSocket clients  
7. React client receives the update and displays it on a map

---

**Tech Stack**

**Backend**
- AWS API Gateway (REST + WebSocket)
- AWS Lambda (Python)
- AWS DynamoDB
- AWS DynamoDB Streams
- FCM integration

**Clients**
- Android (Kotlin, FCM)
- React (Next.JS, WebSocket, MapLibre UI)


---

**Repository Structure**

/android        - Minimal Android client

/client         - Web UI for live tracking

/backend-aws    - Lambda functions + infra

/backend-local  - Local Flask server (deprecated)

Each folder contains its own README with details.

---

**Purpose**

This project is intentionally lightweight.  
It exists to demonstrate:
- Cloud event flow  
- Real‑time updates  
- Mobile → backend → web integration  
- Clean architecture  

It is **not** intended as a production‑ready mobile or web application.


