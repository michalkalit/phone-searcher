# React Client

A lightweight web client that displays real‑time device location updates pushed from the AWS backend.

---

**What the Web Client Does**

- Connects to the AWS WebSocket API
- Listens for location updates from DynamoDB stream → Lambda
- Displays the device location on a map

---

**Code Structure**
src/app

    components/
    
        Spinner/        → Custom SVG/CSS loading animation
        
    hooks/


**How To Run Locally**
npm install
npm run dev

---

**Notes**
The client uses a custom SVG spinner (adapted from CodePen)

Not intended as a production web application

    

