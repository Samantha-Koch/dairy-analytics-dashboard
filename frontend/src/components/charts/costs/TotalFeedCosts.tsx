import Plot from "react-plotly.js";

export default function TotalFeedCostsChart({ data }) {
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
            title: "Total Feed Costs",
            height: 350,
            margin: { t: 40, l: 40, r: 20, b: 40 },
        }}
        />
    );
}