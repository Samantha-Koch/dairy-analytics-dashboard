import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Plotly from "plotly.js-dist-min";

Plot.defaultProps = {
  ...Plot.defaultProps,
  plotly: Plotly,
};

export default function TotalCostsChart({ data }) {
    if (!data || !data.dates || !data.values) {
        return <p style={{fontFamily: "helvetica neue",fontSize: "9pt"}}>No chart data loaded</p>;
      }
    return (
        <Plot
        data={[
            {
            x: data.dates,
            y: data.values,
            type: "scatter",
            mode: "lines+markers",
            },
        ]}
        layout={{
            title: "Total Costs",
            height: 350,
            margin: { t: 40, l: 40, r: 20, b: 40 },
        }}
        />
    );
}