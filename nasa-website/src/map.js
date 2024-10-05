import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";

function Map() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh", // makes the parent div take up the full viewport height
      }}
    >
      {/* Header */}
      <h1 style={{ marginBottom: "20px" }}>Map View</h1>

      {/* Map Container */}
      <div
        style={{
          width: "800px",
          height: "500px",
          border: "1px solid black",
          overflow: "hidden",
        }}
      >
        <MapContainer
          center={[38, -0.09]}
          zoom={5}
          style={{ width: "100%", height: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          />
        </MapContainer>
      </div>
    </div>
  );
}

export default Map;
