export default function KpiValue({ value, unit }) {
    if (value === null || value === undefined) {
      return <p style={styles.noValue}>—</p>;
    }
  
    return (
      <p style={styles.value}>
        {value.toLocaleString(undefined, { maximumFractionDigits: 2 })}{" "}
        <span style={styles.unit}>{unit}</span>
      </p>
    );
  }
  
  const styles = {
    value: {
      fontSize: "20pt",
      fontWeight: 600,
      margin: "6px 0",
    },
    unit: {
      fontSize: "10pt",
      color: "#000000",
      marginLeft: "4px",
    },
    noValue: {
      fontSize: "18pt",
      color: "#000000",
    },
  };
  