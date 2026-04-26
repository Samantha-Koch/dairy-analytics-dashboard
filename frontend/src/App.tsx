import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard";
import HerdPage from "./pages/Herd/HerdPage";
import FeedPage from "./pages/Feed/FeedPage";
import ForecastPage from "./pages/Forecast/ForecastPage";
import DataExplorer from "./pages/DataExplorer/DataExplorer";
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
            <Route path="/herd" element={<HerdPage />} />
            <Route path="/feed" element={<FeedPage />} />
            <Route path="/forecast" element={<ForecastPage />} />
            <Route path="/data" element={<DataExplorer />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
