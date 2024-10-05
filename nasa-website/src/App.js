import "./App.css";
import Map from "./map.js";
import MapComponent from "./MapComponent.js";

import { BrowserRouter, Route, Routes } from "react-router-dom";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Map />} />
        <Route path="/" element={<Map />} />
        <Route path="/mapcomp" element={<MapComponent />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
