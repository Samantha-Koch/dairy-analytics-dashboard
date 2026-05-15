import React, { useEffect, useState } from "react";
import _Plotly from "plotly.js/lib/core";
import _createPlotlyComponent from "react-plotly.js/factory";

import {
  getTotalCostsData,
  getTotalCostsAvailableYears,
} from "../../../services/api/costsService";

import type {
  CostsSource,
  CostsFrequency,
} from "../../../services/api/costsService";

const createPlotlyComponent =
  (_createPlotlyComponent as any).default || _createPlotlyComponent;
const Plot = createPlotlyComponent(_Plotly);

interface Props {
  customerId?: string;
}

export default function TotalCostsChart({ customerId }: Props) {
  const [source, setSource] = useState<CostsSource>("both");
  const [frequency, setFrequency] = useState<CostsFrequency>("annual");
  const [year, setYear] = useState<string>("");
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);

  // Load available years (customer only)
  useEffect(() => {
    getTotalCostsAvailableYears().then((res) => {
      const years = res.years || [];
      setAvailableYears(years);
      if (years.length > 0) {
        setYear(String(years[years.length - 1]));
      }
    });
  }, []);

  // Fetch chart data
  useEffect(() => {
    if (source !== "customer") {
      // USDA or BOTH → always annual, no year needed
      getTotalCostsData({
        source,
        frequency: "annual",
        customerId,
      }).then((res) => setChartData(res.data || []));
      return;
    }

    // CUSTOMER source
    if (frequency === "monthly" && !year) return;

    getTotalCostsData({
      source,
      frequency,
      year,
      customerId,
    }).then((res) => setChartData(res.data || []));
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
      {/* Dropdowns */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "12px" }}>
        {/* Source selector */}
        <select
          value={source}
          onChange={(e) => setSource(e.target.value as CostsSource)}
        >
          <option value="usda">USDA</option>
          <option value="customer">Customer</option>
          <option value="both">Both</option>
        </select>

        {/* Frequency selector (customer only) */}
        {source === "customer" && (
          <select
            value={frequency}
            onChange={(e) => setFrequency(e.target.value as CostsFrequency)}
          >
            <option value="annual">Annual</option>
            <option value="monthly">Monthly</option>
          </select>
        )}

        {/* Year selector (customer + monthly only) */}
        {source === "customer" && frequency === "monthly" && (
          <select value={year} onChange={(e) => setYear(e.target.value)}>
            {availableYears.map((yr) => (
              <option key={yr} value={yr}>
                {yr}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Plot */}
      <Plot
        data={traces}
        layout={{
          title: "Total Costs ($/CWT)",
          xaxis: {
            title: {
              text: source === "customer" && frequency === "monthly" ? "Month" : "Year",
            },
          },
          yaxis: { title: { text: "Total Costs ($/CWT)" } },
          autosize: true,
        }}
        style={{ width: "100%", height: "75%" }}
      />
    </div>
  );
}
