"use client";
import { useState } from "react";
import LoginForm from "./components/LoginForm";
import MapView from "./components/MapView";
import { useDeviceLocation } from "./hooks/useDeviceLocation";
import 'leaflet/dist/leaflet.css';
import { Box } from "@mui/material";

function App() {
  const [phone, setPhone] = useState<string | null>(null);

  if (!phone) {
    return (
      <Box sx={{
        backgroundImage: "url('/foliage.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backdropFilter: "blur(6px)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  }}>
        <LoginForm onLoginSuccess={setPhone} />
      </Box>
    );
  }

  const { data: location, isLoading, error } = useDeviceLocation(phone);

  if (isLoading) {
    return <div>Loading location…</div>;
  }

  if (error) {
    return <div>Failed to load location.</div>;
  }

  if (!location) {
    return <div>Waiting for GPS…</div>;
  }

  return <MapView location={location} />;
}


export default App;
