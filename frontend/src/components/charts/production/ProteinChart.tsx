import React, { useEffect, useState } from "react";
import { getProteinData, getAvailableYears } from "../../../services/api/productionService";
import type { ProductionSource, ProductionFrequency } from "../../../services/api/productionService";
import _Plotly from "plotly.js/lib/core";
import _createPlotlyComponent from "react-plotly.js/factory";
const createPlotlyComponent = (_createPlotlyComponent as any).default || _createPlotlyComponent;
const Plot = createPlotlyComponent(_Plotly);

interface Props {
  customerId?: string;
}

export default function ProteinChart({ customerId }: Props) {
  console.log("ProteinChart mounted");
  const [source, setSource] = useState<ProductionSource>("both");
  const [frequency, setFrequency] = useState<ProductionFrequency>("annual");
  const [year, setYear] = useState<string>("");
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    getAvailableYears("protein").then((res) => {
      const years = res.years || [];
      setAvailableYears(years);
      if (years.length > 0) {
        setYear(String(years[years.length - 1]));
      }
    });
  }, []);

  useEffect(() => {
    console.log("protein useEffect triggered", {source, frequency, year, customerId});
    if (frequency === "monthly" && !year) {
        console.log("protein Blocked because monthly + no year");
        return;
      }

    console.log("Protein Fetching now");
    getProteinData({
      source,
      frequency,
      year,
      customerId,
    }).then((res) => {
      setChartData(res.data || []);
    });
  }, [source, frequency, year, customerId]);

  if (!chartData || chartData.length === 0) {
    return (
      <p style={{ fontFamily: "helvetica neue", fontSize: "9pt" }}>
        No chart data loaded
      </p>
    );
  }

  const xValues = chartData.map((row) => row.time);
  const usdaValues = chartData.map((row) => row.usda_value);
  const customerValues = chartData.map((row) => row.customer_value);

  const traces: any[] = [];
  if (source !== "customer") {
    traces.push({
      x: xValues,
      y: usdaValues,
      type: "scatter",
      mode: "lines+markers",
      name: "USDA",
      line: { color: "#2d2d2d" },
    });
  }
  if (source !== "usda") {
    traces.push({
      x: xValues,
      y: customerValues,
      type: "scatter",
      mode: "lines+markers",
      name: "Customer",
      line: { color: "#0077cc" },
    });
  }

  return (
    <div>
      <div style={{ display: "flex", gap: "12px", marginBottom: "12px" }}>
        <select value={source} onChange={(e) => setSource(e.target.value as ProductionSource)}>
          <option value="usda">USDA</option>
          <option value="customer">Customer</option>
          <option value="both">Both</option>
        </select>

        <select
          value={frequency}
          onChange={(e) => setFrequency(e.target.value as ProductionFrequency)}
        >
          <option value="annual">Annual</option>
          <option value="monthly">Monthly</option>
        </select>

        {frequency === "monthly" && (
          <select value={year} onChange={(e) => setYear(e.target.value)}>
            {availableYears.map((yr) => (
              <option key={yr} value={yr}>
                {yr}
              </option>
            ))}
          </select>
        )}
      </div>

      <Plot
        data={traces}
        layout={{
          title: "Protein Percentage",
          xaxis: { title: {text: frequency === "annual" ? "Year" : "Month"} },
          yaxis: { title: {text: "Protein (%)" }},
          autosize: true,
        }}
        style={{ width: "100%", height: "75%" }}
      />
    </div>
  );
}
