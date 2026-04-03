import { useRef } from "react";
import { Location } from "../hooks/useDeviceLocation";
import { useMap } from "../hooks/useMap";
import 'leaflet/dist/leaflet.css';

interface Props {
  location: Location | null;
}

export default function MapView({ location }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useMap(containerRef, location);

  return (
    <div
      ref={containerRef}
    />
  );
}
