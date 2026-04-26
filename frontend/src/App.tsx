import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard";
import ProductionPage from "./pages/Production/ProductionPage";
import MarketDataPage from "./pages/MarketData/MarketDataPage";
import DataUpload from "./pages/DataUpload/DataUpload";
import Costs from "./pages/Costs/Costs";
import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";
import React from "react";

function App() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <Topbar />

        <div style={{ padding: "20px", overflowY: "auto" }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/production" element={<ProductionPage />} />
            <Route path="/costs" element={<Costs />} />
            <Route path="/market-data" element={<MarketDataPage />} />
            <Route path="/data-upload" element={<DataUpload />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
