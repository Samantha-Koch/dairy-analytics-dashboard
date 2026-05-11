import React from 'react';
import { getMilkClassPrices} from "../../../services/api/marketDataService";
import { useEffect, useState } from "react";
import Plotly from 'plotly.js/lib/core';
import createPlotlyComponent from 'react-plotly.js/factory';

// This line is the magic fix for the "got: object" error
const Plot = (createPlotlyComponent as any).default ? (createPlotlyComponent as any).default(Plotly) : createPlotlyComponent(Plotly);



export default function MilkClassChart() {
    const [year, setYear] = useState("all");
    const [chartData, setChartData] = useState([]);

    useEffect(() =>{
        getMilkClassPrices(year).then((res) => {
            console.log("Milk class API response:", res.data);
            console.log("Milk class chartData:", res.data);
            setChartData(res.data);
        });
    }, [year]);

    if (!chartData || chartData.length === 0) {
        return <p style={{fontFamily: "helvetica neue",fontSize: "9pt"}}>No chart data loaded</p>;
      }
    
    const xValues = chartData.map(row => row.time || row.year);
    const classI = chartData.map((row) => row.class_i);
    const classII = chartData.map((row) => row.class_ii);
    const classIII = chartData.map((row) => row.class_iii);
    const classIV = chartData.map((row) => row.class_iv);

    return (
        <div>
            <select 
                value={year}
                onChange={(e) => setYear(e.target.value)}
                style={{ marginBottom: "10px"}}
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
                    y: classI,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Class I",
                    line: {color: "6b6b6b"}
                },
                {
                    x: xValues,
                    y: classII,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Class II",
                    line: {color: "#2d2d2d" }
                },
                {
                    x: xValues,
                    y: classIII,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Class III",
                    line: {color: "2196F3"}
                },
                {
                    x: xValues,
                    y: classIV,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Class IV",
                    line: {color: "0066b3"}
                },
                ]}
                layout={{
                    title: "Milk Class Price Trends",
                    xaxis: {title: {text: year === "all" ? "Year" : "Month"}},
                    yaxis: {title: {text: "Price ($/cwt)"}},
                    autosize: true,
                }}
                style={{width: "100%", height: "75%"}}
            />
        </div>
    );
}