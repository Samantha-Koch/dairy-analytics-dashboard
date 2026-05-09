export default function KpiDropdown({
  view,
  setView,
  hasUsdaData = false,
  hasCustomerData = false,
}) {

  const options = [];

  if (hasCustomerData) {
    options.push({ key: "customer_avg", label: "Customer Average" });
    options.push({ key: "customer_trend", label: "Customer Trend" });
  }

  if (hasUsdaData) {
    options.push({ key: "usda_avg", label: "USDA Average" });
  }

  // If no data disable dropdown
  const noOptions = options.length === 0;

  // Ensure current view is valid
  const safeView = options.some(o => o.key === view)
    ? view
    : options[0]?.key ?? "";

  return (
    <select
      value={safeView}
      onChange={(e) => setView(e.target.value)}
      disabled={noOptions}
      style={styles.dropdown}
    >
      {noOptions ? (
        <option>No data</option>
      ) : (
        options.map((opt) => (
          <option key={opt.key} value={opt.key}>
            {opt.label}
          </option>
        ))
      )}
    </select>
  );
}

const styles = {
  dropdown: {
    fontSize: "8pt",
    padding: "2px 4px",
    borderRadius: "4px",
    fontFamily: "helvetica neue",
  },
};
