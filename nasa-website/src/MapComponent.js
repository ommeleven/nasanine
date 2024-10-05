import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Fix for missing marker icons in Leaflet
import L from "leaflet";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

let DefaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconAnchor: [12, 41], // This anchors the icon to the correct spot
});

L.Marker.prototype.options.icon = DefaultIcon;

const markersData = [
  {
    position: [36.5332, -76.9117],
    popupContent: "Site: ACT Elevation: 5599.0m",
  },
  {
    position: [36.3336, -77.1419],
    popupContent: "Site: ACT Elevation: 333.0m",
  },
  {
    position: [36.4011, -77.0741],
    popupContent: "Site: ACT Elevation: 949.0m",
  },
  {
    position: [36.4645, -77.4188],
    popupContent: "Site: ACT Elevation: 3341.0m",
  },
];

const MapComponent = () => {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <MapContainer
        center={[36.4331, -77.1366]}
        zoom={6}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {markersData.map((marker, index) => (
          <Marker key={index} position={marker.position}>
            <Popup>{marker.popupContent}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
