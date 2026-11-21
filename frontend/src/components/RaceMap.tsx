"use client";

import { useEffect, useRef } from "react";
import { TrainLivePerformance } from "@/lib/types";
import { Map, Navigation } from "lucide-react";

interface Props {
  train1: TrainLivePerformance;
  train2: TrainLivePerformance;
  destinationName: string;
  destinationCode: string;
  destLat?: number | null;
  destLng?: number | null;
}

export default function RaceMap({
  train1,
  train2,
  destinationName,
  destinationCode,
  destLat,
  destLng,
}: Props) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window === "undefined" || !mapContainerRef.current) return;

    // Load leaflet dynamically
    let isMounted = true;
    import("leaflet").then((L) => {
      if (!isMounted || !mapContainerRef.current) return;

      // Include Leaflet CSS dynamically if not present
      if (!document.getElementById("leaflet-css")) {
        const link = document.createElement("link");
        link.id = "leaflet-css";
        link.rel = "stylesheet";
        link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
        document.head.appendChild(link);
      }

      // Coordinates
      const t1Lat = train1.current_lat || 17.9689;
      const t1Lng = train1.current_lng || 79.5941;
      const t2Lat = train2.current_lat || 17.9787;
      const t2Lng = train2.current_lng || 79.5255;
      const dLat = destLat || 17.5986;
      const dLng = destLng || 80.0033;

      if (!mapInstanceRef.current) {
        const map = L.map(mapContainerRef.current, {
          attributionControl: false,
        }).setView([dLat, dLng], 9);

        L.tileLayer(
          "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
          {
            maxZoom: 18,
          }
        ).addTo(map);

        mapInstanceRef.current = map;
      }

      const map = mapInstanceRef.current;

      // Clear existing layers
      map.eachLayer((layer: any) => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
          map.removeLayer(layer);
        }
      });

      // Markers
      const createIcon = (color: string, label: string) =>
        L.divIcon({
          className: "custom-div-icon",
          html: `<div style="background-color: ${color}; color: #000; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 9999px; border: 2px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 4px; white-space: nowrap;">🚆 ${label}</div>`,
          iconSize: [80, 26],
          iconAnchor: [40, 13],
        });

      const destIcon = L.divIcon({
        className: "custom-div-icon",
        html: `<div style="background-color: #10b981; color: #000; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 9999px; border: 2px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 4px; white-space: nowrap;">🏁 ${destinationCode}</div>`,
        iconSize: [60, 26],
        iconAnchor: [30, 13],
      });

      // Add Train 1
      const m1 = L.marker([t1Lat, t1Lng], {
        icon: createIcon("#00f0ff", train1.train_number),
      })
        .addTo(map)
        .bindPopup(`<b>Train ${train1.train_number}</b><br>${train1.train_name}<br>Speed: ${train1.current_speed_kmh} km/h`);

      // Add Train 2
      const m2 = L.marker([t2Lat, t2Lng], {
        icon: createIcon("#c084fc", train2.train_number),
      })
        .addTo(map)
        .bindPopup(`<b>Train ${train2.train_number}</b><br>${train2.train_name}<br>Speed: ${train2.current_speed_kmh} km/h`);

      // Add Destination
      const md = L.marker([dLat, dLng], { icon: destIcon })
        .addTo(map)
        .bindPopup(`<b>Destination: ${destinationName} (${destinationCode})</b>`);

      // Route lines
      L.polyline([[t1Lat, t1Lng], [dLat, dLng]], {
        color: "#00f0ff",
        weight: 3,
        dashArray: "6, 8",
        opacity: 0.8,
      }).addTo(map);

      L.polyline([[t2Lat, t2Lng], [dLat, dLng]], {
        color: "#c084fc",
        weight: 3,
        dashArray: "6, 8",
        opacity: 0.8,
      }).addTo(map);

      // Fit bounds
      const group = L.featureGroup([m1, m2, md]);
      map.fitBounds(group.getBounds().pad(0.3));
    });

    return () => {
      isMounted = false;
    };
  }, [train1, train2, destLat, destLng, destinationName, destinationCode]);

  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 mb-8 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Map className="w-4 h-4 text-rail-cyan" />
            <span>Live Geospatial Convergence Map</span>
          </h3>
          <p className="text-xs text-slate-400">
            OpenStreetMap live satellite & track projection towards {destinationName} ({destinationCode})
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <Navigation className="w-3.5 h-3.5 text-rail-cyan" />
          <span>Live GPS Telemetry</span>
        </div>
      </div>

      <div
        ref={mapContainerRef}
        className="w-full h-80 sm:h-96 rounded-xl overflow-hidden border border-surface-border z-0"
      />
    </div>
  );
}
