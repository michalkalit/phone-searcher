import { useEffect, useRef, useState } from "react";

export interface Location {
  latitude: number;
  longitude: number;
}

export function useDeviceLocation(phoneNumber: string | null) {
  const [location, setLocation] = useState<Location | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!phoneNumber) return;

    const encoded = encodeURIComponent(phoneNumber);
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}?phoneNumber=${encoded}`;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.latitude && data.longitude) {
          setLocation({
            latitude: data.latitude,
            longitude: data.longitude,
          });
        }
      } catch (err) {
        console.error("Invalid WS message:", err);
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => {
      ws.close();
    };
  }, [phoneNumber]);

  return location;
}
