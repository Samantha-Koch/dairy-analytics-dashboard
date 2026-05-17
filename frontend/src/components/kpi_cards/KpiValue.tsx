import type {CSSProperties} from "react";
export default function KpiValue({ value, unit }) {
  // Case 1: No value
  if (value === null || value === undefined) {
    return <p style={styles.noValue}>—</p>;
  }

  // Case 2: USDA object (milk class)
// Case: Milk Class Prices (object)
if (typeof value === "object") {
  const labelMap: Record<string, string> = {
    ClassIWhole: "Class 1",
    ClassIIWhole: "Class 2",
    ClassIIIWhole: "Class 3",
    ClassIVWhole: "Class 4",
  };

  return (
    <div style={styles.stackContainer}>
      {Object.entries(value).map(([key, val]) => {
        const label = labelMap[key] ?? key;

        return (
          <div key={key} style={styles.stackBlock}>
            <div style={styles.stackLabel}>{label}:</div>
            <div style={styles.stackValue}>
              {typeof val === "number"
                ? val.toLocaleString(undefined, { maximumFractionDigits: 2 })
                : "—"}
              {unit && typeof val === "number" ? ` ${unit}` : ""}
            </div>
          </div>
        );
      })}
    </div>
  );
}


  // Case 3: Normal numeric KPI
  if (typeof value === "number") {
    return (
      <p style={styles.value}>
        {value.toLocaleString(undefined, { maximumFractionDigits: 2 })}{" "}
        <span style={styles.unit}>{unit}</span>
      </p>
    );
  }

  // Fallback
  return <p style={styles.noValue}>—</p>;
}


const styles: {
  value: CSSProperties;
  unit: CSSProperties;
  noValue: CSSProperties;
  stackContainer: CSSProperties;
  stackBlock: CSSProperties;
  stackLabel: CSSProperties;
  stackValue: CSSProperties;
} = {
  value: {
    fontSize: "14pt",
    fontWeight: 600,
    margin: "6px 6px",
  },
  unit: {
    fontSize: "10pt",
    color: "#000000",
    marginLeft: "4px",
  },
  noValue: {
    fontSize: "12pt",
    color: "#000000",
  },
  stackContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginTop: "6px",
  },
  stackBlock: {
    display: "flex",
    flexDirection: "column",
  },
  stackLabel: {
    fontWeight: 600,
    fontSize: "12pt",
  },
  stackValue: {
    fontWeight: 500,
    fontSize: "12pt",
    marginLeft: "4px",
  },
};

