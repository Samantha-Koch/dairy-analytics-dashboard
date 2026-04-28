import Plot from "react-plotly.js";

export default function MilkFeedRatioChart({ data }) {
    if (!data || !data.dates || !data.values) {
        return <p>No chart data loaded</p>;
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
            title: "Milk to Feed Ratio",
            height: 350,
            margin: { t: 40, l: 40, r: 20, b: 40 },
        }}
        />
    );
}