import React from 'react';
import { useEffect, useState } from "react";
import Plotly from 'plotly.js/lib/core';
import createPlotlyComponent from 'react-plotly.js/factory';

// This line is the magic fix for the "got: object" error
const Plot = (createPlotlyComponent as any).default ? (createPlotlyComponent as any).default(Plotly) : createPlotlyComponent(Plotly);



export default function AvgMilkYieldChart({ data }) {
    const [source, setSource] = useState("USDA");
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        getAvgMilkYield(source).then((res) => {
            console.log("Yield API response:", res.data);
            console.log("Yield chartData:", res.data);
            setChartData(res.data);
        });
    }, [source]);

    if (!chartData || chartData.length === 0) {
        return (
            <p style={{ fontFamily: "helvetica neue", fontSize: "9pt" }}>
                No chart data loaded
            </p>
        );
    }

    const xValues = chartData.map(row => row.source_period || row.year);
    const yValues = chartData.map((row) => row.milk_yield);

    return (
        <div>
            <select
                value={source}
                onChange={(e) => setSource(e.target.value)}
                style={{ marginBottom: "10px" }}
            >
                <option value="USDA">"USDA"</option>
                <option value="Individual Farm">"Individual Farm"</option>
            </select>

            <Plot
                data={[
                {
                    x: xValues,
                    y: yValues,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Average Monthly Milk Yield Per Cow",
                    line: {color: "#2d2d2d"}
                },
                ]}
                layout={{
                title: "Cheese Price Trends",
                xaxis: { title: "Year" },
                yaxis: { title: "Pounds" },
                autosize: true,
                }}
                style={{ width: "100%", height: "75%" }}
            />
        </div>
    );
}
