import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard";
import Costs from "./pages/Costs/Costs";
import Sidebar from "./components/layout/Sidebar";
import Production from "./pages/Production/ProductionPage";
import MarketData from "./pages/MarketData/MarketDataPage";
import DataUpload from "./pages/DataUpload/DataUpload";
function App() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar/>
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>  
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/production" element={<Production />} />
            <Route path="/costs" element={<Costs />} />
            <Route path="/marketdata" element={<MarketData />} />
            <Route path="/dataupload" element={<DataUpload />} />
          </Routes>
      </div>
    </div>
  );
}

export default App;
