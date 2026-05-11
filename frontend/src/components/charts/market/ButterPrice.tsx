import React from 'react';
import { useEffect, useState } from "react";
import { getButterPrices } from "../../../services/api/marketDataService";
import _Plotly from "plotly.js/lib/core";
import _createPlotlyComponent from 'react-plotly.js/factory';
const createPlotlyComponent = (_createPlotlyComponent as any).default || _createPlotlyComponent;
const Plot = createPlotlyComponent(_Plotly);



export default function ButterPriceChart() {
  const [year, setYear] = useState("all");
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    getButterPrices(year).then((res) => {
      console.log("butter API response:", res.data);
      console.log("butter chartData:", res.data);
      setChartData(res.data);
    });
  }, [year]);

  if (!chartData || chartData.length === 0) {
    return (
      <p style={{ fontFamily: "helvetica neue", fontSize: "9pt" }}>
        No chart data loaded
      </p>
    );
  }

  const xValues = chartData.map(row => row.time_id || row.year);
  const yValues = chartData.map((row) => row.butter_price);

  return (
    <div>
      <select
        value={year}
        onChange={(e) => setYear(e.target.value)}
        style={{ marginBottom: "10px" }}
      >
        <option value="all">All Years</option>
        <option value="2025">2025</option>
        <option value="2026">2026</option>
      </select>

      <Plot
        data={[
          {
            x: xValues,
            y: yValues,
            type: "scatter",
            mode: "lines+markers",
            name: "Butter Price",
            line: {color: "#2d2d2d"}
          },
        ]}
        layout={{
          title: "Butter Price Trends",
          xaxis: { title: {text: year === "all" ? "Year" : "Month" }},
          yaxis: { title: {text: "Price ($/lb)" }},
          autosize: true,
        }}
        style={{ width: "100%", height: "75%" }}
      />
    </div>
  );
}
