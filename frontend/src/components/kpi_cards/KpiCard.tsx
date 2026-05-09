import { useState, useEffect } from "react";
import KpiValue from "./KpiValue";
import KpiDropdown from "./KpiDropdown";
import KpiTrendSparkline from "./KpiTrendSparkline";

export default function KpiCard({ title, data }) {
  // Always start with customer_avg unless USDA-only
  const [view, setView] = useState("customer_avg");

  // Update view when data arrives
  useEffect(() => {
    if (!data) return;

    if (data.customer_data_exists) {
      setView("customer_avg");
    } else if (data.has_usda_data) {
      setView("usda_avg");
    }
  }, [data]);

  // Safe accessors — these CANNOT crash
  const safeValue = data?.[view] ?? "--";
  const safeDates = Array.isArray(data?.dates) ? data.dates : [];
  const safeTrend = Array.isArray(data?.[`${view}_trend`])
    ? data[`${view}_trend`]
    : [];

  const hasUsda = data?.has_usda_data ?? false;
  const hasCustomer = data?.customer_data_exists ?? false;
  const unit = data?.unit ?? "";

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <h3 style={styles.title}>{title}</h3>

        <KpiDropdown
          view={view}
          setView={setView}
          hasUsdaData={hasUsda}
          hasCustomerData={hasCustomer}
        />
      </div>

      <KpiValue value={safeValue} unit={unit} />

      <KpiTrendSparkline dates={safeDates} values={safeTrend} />
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
    fontSize: "14pt",
    fontWeight: 600,
  },
};
