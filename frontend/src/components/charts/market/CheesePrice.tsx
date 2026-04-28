import Plot from "react-plotly.js";

export default function CheesePriceChart({ data }) {
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
            title: "Cheese Price Trends",
            height: 350,
            margin: { t: 40, l: 40, r: 20, b: 40 },
        }}
        />
    );
}