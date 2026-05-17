import { useState, useEffect } from "react";
import KpiValue from "./KpiValue";
import KpiDropdown from "./KpiDropdown";
import KpiTrendSparkline from "./KpiTrendSparkline";
import type { CSSProperties } from "react";

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
  const safeDates =
  view.startsWith("customer")
    ? Array.isArray(data?.dates) ? data.dates : []
    : Array.isArray(data?.usda_dates) ? data.usda_dates : [];
  const hasUsda = data?.has_usda_data ?? false;
  const hasCustomer = data?.customer_data_exists ?? false;
  const unit = data?.unit ?? "";

  // Trend should follow the data source, not the specific view key
  const safeTrend =
  view.startsWith("customer")
    ? Array.isArray(data?.customer_trend) ? data.customer_trend : []
    : Array.isArray(data?.usda_trend) ? data.usda_trend : [];

  // Compute percent change for customer trend
  let percentChange = null;

  if (view === "customer_trend" && safeTrend.length > 1) {
    const last12 = safeTrend.slice(-12);
    const current = last12[last12.length - 1];
    const previousAvg =
      last12.length > 1
        ? last12.slice(0, -1).reduce((a, b) => a + b, 0) / (last12.length - 1)
        : null;

    if (previousAvg && previousAvg !== 0) {
      percentChange = ((current - previousAvg) / previousAvg) * 100;
    }
  }

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

      {/* ⭐ Only show numeric value in customer_avg or usda_avg */}
      {view !== "customer_trend" && (
        <KpiValue value={safeValue} unit={unit} />
      )}

      {view === "customer_trend" &&(
        <KpiTrendSparkline dates={safeDates} values={safeTrend} />
      )}
      {view === "customer_trend" && percentChange !== null && (
        <div style={styles.percentChange}>
          {percentChange > 0 ? "+" : ""}
          {percentChange.toFixed(1)}%
        </div>
      )}

    </div>
  );
}


const styles: {
  card: CSSProperties;
  header: CSSProperties;
  title: CSSProperties;
  percentChange: CSSProperties;
} = {
  card: {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "12px",
    width: "75%",
    fontFamily: "helvetica neue",
    backgroundColor: "white",

    // ⭐ Center everything
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    textAlign: "center",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    width: "100%", // keeps dropdown aligned
    marginBottom: "8px",
  },
  title: {
    margin: 0,
    fontSize: "14pt",
    fontWeight: 600,
  },
  percentChange: {
    marginTop: "4px",
    fontSize: "12pt",
    fontWeight: 600,
  },  
};

