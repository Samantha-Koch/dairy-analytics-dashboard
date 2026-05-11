import React from 'react';
import { useEffect, useState } from "react";
import { getMilkCompPrices } from "../../../services/api/marketDataService";
import Plotly from 'plotly.js/lib/core';
import createPlotlyComponent from 'react-plotly.js/factory';

// This line is the magic fix for the "got: object" error
const Plot = (createPlotlyComponent as any).default ? (createPlotlyComponent as any).default(Plotly) : createPlotlyComponent(Plotly);



export default function MilkCompChart() {
  const [year, setYear] = useState("all");
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    getMilkCompPrices(year).then((res) => {
      console.log("Milk comp API response:", res.data);
      console.log("Milk comp chartData:", res.data);
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

  // X-axis: date or year
  const xValues = chartData.map(row => row.time || row.year);

  // Y-axis series
  const butterfat = chartData.map((row) => row.butterfat);
  const protein = chartData.map((row) => row.protein);

  return (
    <div>
      <select
        value={year}
        onChange={(e) => setYear(e.target.value)}
        style={{ marginBottom: "10px" }}
      >
        <option value="all">All Years</option>
        <option value="2020">2020</option>
        <option value="2021">2021</option>
        <option value="2022">2022</option>
        <option value="2023">2023</option>
        <option value="2024">2024</option>
        <option value="2025">2025</option>
        <option value="2026">2026</option>
      </select>

      <Plot
        data={[
          {
            x: xValues,
            y: butterfat,
            type: "scatter",
            mode: "lines+markers",
            name: "Butterfat",
            line: {color: "#2d2d2d"}
          },
          {
            x: xValues,
            y: protein,
            type: "scatter",
            mode: "lines+markers",
            name: "Protein",
            line: {color: "#0056b3"}
          },
        ]}
        layout={{
          title: "Milk Component Price Trends",
          xaxis: { title: {text: year === "all" ? "Year" : "Month" }},
          yaxis: { title: {text: "Price ($/lb)" }},
          autosize: true,
        }}
        style={{ width: "100%", height: "75%" }}
      />
    </div>
  );
}
