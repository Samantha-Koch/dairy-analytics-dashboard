import Plot from "react-plotly.js";

export default function KpiTrendSparkline({ dates, values }) {
  if (!dates || !values || values.length === 0) {
    return <div style={styles.placeholder}>—</div>;
  }

  return (
    <Plot
      data={[
        {
          x: dates,
          y: values,
          type: "scatter",
          mode: "lines",
          line: {
            color: "#3b82f6",
            width: 2,
          },
          hoverinfo: "skip",
        },
      ]}
      layout={{
        height: 50,
        margin: { t: 5, b: 5, l: 5, r: 5 },
        xaxis: { visible: false },
        yaxis: { visible: false },
        showlegend: false,
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
      }}
      config={{
        displayModeBar: false,
        responsive: true,
      }}
      style={{ width: "100%" }}
    />
  );
}

const styles = {
  placeholder: {
    height: "50px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#aaa",
    fontSize: "10pt",
  },
};
