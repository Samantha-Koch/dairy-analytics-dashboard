import { useEffect, useState } from "react"; 
import MarginCowChart from "../../components/charts/costs/MarginCow";
import MilkFeedRatioChart from "../../components/charts/costs/MilkFeedRatio";
import NetRevenueChart from "../../components/charts/costs/NetRevenue";
import TotalCostsChart from "../../components/charts/costs/TotalCosts";
import TotalFeedCostsChart from "../../components/charts/costs/TotalFeedCosts";
import PageTopbar from "../../components/layout/PageTopbar"

export default function Costs() {
  const sections = [
    { id: "costs", label: "Costs" },
    { id: "feed-trends", label: "Feed Trends" },
    { id: "revenue", label: "Revenue" },
  ];
  const handleSelect = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return;
  
    el.scrollIntoView({
      behavior: "smooth",
      block: "start",
    })
  };

  const [customerEmail, setCustomerEmail] = useState<string>("");

  return (
    <>
      <PageTopbar 
        title="Costs & Revenue"
        sections={sections}
        onSelect={handleSelect}
      />
      <div style={{padding: "0px 20px 20px 40px", overflowY:"auto", height:"100%"}}>
        <Section title="Costs & Revenue">
          <CustomerFilterCard
              email={customerEmail}
              onEmailChange={setCustomerEmail}
          />

          <SubTitle id="costs" title="Costs"></SubTitle>
          <Subsection title="Total Costs">
            <TotalCostsChart customerId={customerEmail || undefined} />
          </Subsection>

          <SubGroup id="feed-trends" title="Feed Trends"></SubGroup>
          <Subsection title="Total Feed Costs">
            <TotalFeedCostsChart customerId={customerEmail || undefined} />  
          </Subsection>
      
          <Subsection title="Milk to Feed Ratio">
            <MilkFeedRatioChart customerId={customerEmail || undefined} />
          </Subsection>
      
          <SubTitle id="revenue" title="Revenue"></SubTitle>
          <Subsection title="Net Revenue">
            <NetRevenueChart customerId={customerEmail || undefined} />
          </Subsection>
          <Subsection title="Margin per Cow">
            <MarginCowChart customerId={customerEmail || undefined} />
          </Subsection>
        </Section>
      </div>
    </>  
  );
  
}
function Section({title, children}: any){
  return(
    <div style={{marginTop: ".5%",fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {children}
    </div>
  )
}
function Subsection({title, children}: any){
  return(
    <div style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "12pt"}}>
      {title}
      {children}
    </div>
  )
}
function SubGroup({id, title, children}: any){
  return(
    <div id={id} style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "14pt"}}>
      {title}
      {children}
    </div>
  )
}
function SubTitle({id, title, children}: any){
  return(
    <div id={id} style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {title}
      {children}
    </div>
  )
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
