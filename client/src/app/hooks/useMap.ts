import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { Location } from "./useDeviceLocation";
let rtlPluginLoaded = false;
import "maplibre-gl/dist/maplibre-gl.css";


export function useMap(container: React.RefObject<HTMLDivElement>, location: Location | null) {
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markerRef = useRef<maplibregl.Marker | null>(null);




  useEffect(() => {
    if (rtlPluginLoaded) return;
    maplibregl.setRTLTextPlugin(
      "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js",
      true
    );
    rtlPluginLoaded = true;

  }, []);


  useEffect(() => {
    if (!container.current || !rtlPluginLoaded || mapRef.current) return;

    mapRef.current = new maplibregl.Map({
      container: container.current,
      style:
        "https://maps.geoapify.com/v1/styles/osm-bright/style.json?apiKey=a407ebf95b2a4e9ba0e01805a1a22d42",
      center: [35.0853, 31.7818],
      zoom: 13,
      attributionControl: false,
    });
  }, [container, rtlPluginLoaded]);

useEffect(() => {
  if (!mapRef.current || !location) return;

  const { latitude, longitude } = location;
  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number" ||
    Number.isNaN(latitude) ||
    Number.isNaN(longitude)
  ) {
  console.warn("Invalid coordinates:", location);
  return;
}
  // Remove previous marker
  if (markerRef.current) {
    markerRef.current.remove();
  }

  // Animate to the new location
  mapRef.current.flyTo({
    center: [longitude, latitude],
    zoom: 13,
    essential: true,
  });

  // Wait for the animation to finish
  const onMoveEnd = () => {
    markerRef.current = new maplibregl.Marker()
      .setLngLat([longitude, latitude])
      .setPopup(
        new maplibregl.Popup({ offset: 10, anchor: "top" }).setText(
          `Lat: ${latitude.toFixed(6)}, Lon: ${longitude.toFixed(6)}`
        )
      )
      .addTo(mapRef.current!);

    markerRef.current.togglePopup();

    // Remove listener so it doesn't fire again
    mapRef.current?.off("moveend", onMoveEnd);
  };

  mapRef.current.on("moveend", onMoveEnd);
}, [location]);



  return mapRef;
}
