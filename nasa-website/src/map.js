import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";

function Map() {
  return (
    <div style={{ width: "500px", height: "500px", border: "1px solid black" }}>
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        style={{ width: "100%", height: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        />
      </MapContainer>
    </div>
  );
}

export default Map;
