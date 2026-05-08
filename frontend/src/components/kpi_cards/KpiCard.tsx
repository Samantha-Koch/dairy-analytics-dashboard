import { useState, useEffect } from "react";
import KpiValue from "./KpiValue";
import KpiDropdown from "./KpiDropdown";
import KpiTrendSparkline from "./KpiTrendSparkline"

export default function KpiCard({ title, data }) {
  // Default view depends on whether USDA data exists
  const [view, setView] = useState(() => {
    if (data?.customer_data_exists) return "customer_avg";
    if (data?.has_usda_data) return "usda_avg";
  });

  // Reset view when KPI changes
  useEffect(() => {
    if (data) {
      setView(data.has_usda_data ? "usda_avg" : "customer_avg");
    }
  }, [data]);

  if (!data) {
    return (
      <div style={styles.card}>
        <p style={styles.noData}>No KPI data loaded</p>
      </div>
    );
  }

  const displayedValue = data[view];

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <h3 style={styles.title}>{title}</h3>

        <KpiDropdown
          view={view}
          setView={setView}
          hasUsdaData={data.has_usda_data}
          hasCustomerData={data.customer_data_exists}
        />
      </div>

      <KpiValue value={displayedValue} unit={data.unit} />

      {/* Sparkline placeholder for later */}
      {/* <KpiSparkline dates={data.dates} values={data.values} /> */}
      <KpiTrendSparkline dates={data.dates} values={data[view + "_trend"]} />
        {view.includes("trend") && (
            <KpiTrendSparkline
            dates={data.dates}
            values={data[view]}
            />
        )}
     
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "12px",
    width: "220px",
    fontFamily: "helvetica neue",
    backgroundColor: "white",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "8px",
  },
  title: {
    margin: 0,
    fontSize: "11pt",
    fontWeight: 600,
  },
  noData: {
    fontSize: "9pt",
    color: "#000000",
  },
};
