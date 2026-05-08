export default function KpiDropdown({ view, setView, hasUsdaData, hasCustomerData }) {
    return (
      <select
        value={view}
        onChange={(e) => setView(e.target.value)}
        style={styles.dropdown}
      >
        {hasCustomerData && (
          <>
            <option value="customer_avg">Customer Average</option>
            <option value="customer_trend">Customer Trend</option>
          </>
        )}
  
        {hasUsdaData && (
          <option value="usda_avg">USDA Average</option>
        )}
      </select>
    );
  }
  
  const styles = {
    dropdown: {
      fontSize: "9pt",
      padding: "2px 4px",
      borderRadius: "4px",
      border: "1px solid #ccc",
      backgroundColor: "white",
    },
  };
  