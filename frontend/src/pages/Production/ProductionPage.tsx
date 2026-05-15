import { useState } from "react";
import AvgMilkYieldChart from "../../components/charts/production/AvgMilkYieldChart";
import SccChart from "../../components/charts/production/SccChart";
import ButterfatChart from "../../components/charts/production/ButterfatChart";
import ProteinChart from "../../components/charts/production/ProteinChart";
import PageTopbar from "../../components/layout/PageTopbar";

export default function Production() {
  const sections = [
    { id: "milk-yield", label: "Average Milk Yield Per Cow" },
    { id: "scc", label: "Bulk Tank SCC" },
    { id: "butterfat", label: "Butterfat Percentage" },
    { id: "protein", label: "Protein Percentage" },
  ];

  const handleSelect = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return;

    el.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const [customerEmail, setCustomerEmail] = useState<string>("");

  return (
    <>
      <PageTopbar title="Production" sections={sections} onSelect={handleSelect} />
      <div style={{ padding: "0px 20px 20px 40px", overflowY: "auto", height: "100%" }}>
        <Section title="Production">
          <CustomerFilterCard
            email={customerEmail}
            onEmailChange={setCustomerEmail}
          />

          <Subsection id="milk-yield" title="Average Monthly Milk Yield Per Cow">
            <AvgMilkYieldChart customerId={customerEmail || undefined} />
          </Subsection>

          <Subsection id="scc" title="Bulk Tank SCC">
            <SccChart customerId={customerEmail || undefined} />
          </Subsection>

          <Subsection id="butterfat" title="Butterfat Percentage">
            <ButterfatChart customerId={customerEmail || undefined} />
          </Subsection>

          <Subsection id="protein" title="Protein Percentage">
            <ProteinChart customerId={customerEmail || undefined} />
          </Subsection>
        </Section>
      </div>
    </>
  );
}

function Section({ title, children }: any) {
  return (
    <div style={{ marginTop: ".5%", fontFamily: "helvetica neue", fontSize: "20pt" }}>
      {children}
    </div>
  );
}

function Subsection({ id, title, children }: any) {
  return (
    <div
      id={id}
      style={{ marginTop: "40px", fontFamily: "helvetica neue", fontSize: "20pt" }}
    >
      {title}
      {children}
    </div>
  );
}

interface CustomerFilterProps {
  email: string;
  onEmailChange: (value: string) => void;
}

function CustomerFilterCard({ email, onEmailChange }: CustomerFilterProps) {
  const [localEmail, setLocalEmail] = useState(email);

  const handleApply = () => {
    onEmailChange(localEmail.trim());
  };

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "12px 16px",
        marginBottom: "24px",
        fontFamily: "helvetica neue",
        fontSize: "11pt",
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: "8px" }}>
        Customer Data Filter
      </div>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        <label style={{ fontSize: "10pt" }}>Email:</label>

        <input
          type="email"
          value={localEmail}
          onChange={(e) => setLocalEmail(e.target.value)}
          placeholder="customer@example.com"
          style={{
            flex: 1,
            padding: "6px 8px",
            borderRadius: "4px",
            border: "1px solid #ccc",
            fontSize: "10pt",
          }}
        />

        <button
          onClick={handleApply}
          style={{
            padding: "6px 12px",
            borderRadius: "4px",
            border: "1px solid #0077cc",
            backgroundColor: "#0077cc",
            color: "white",
            cursor: "pointer",
            fontSize: "10pt",
            fontFamily: "helvetica neue",
          }}
        >
          Enter
        </button>
      </div>
    </div>
  );
}

