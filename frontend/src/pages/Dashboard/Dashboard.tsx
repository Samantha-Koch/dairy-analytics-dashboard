import { useEffect, useState } from "react";
import { getDashboardSummary } from "../../services/api/dashboardService";

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load dashboard summary", err);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return <p>Loading...</p>
  }
  if (!summary) {
    return <p>Failed to load dashboard data</p>
  }
  /* link in kpi data where value="add in" is*/
  return (
    <div style={{padding: "20px"}}>
      <h1>Dairy Analytics Dashboard</h1>    
      {/* Section 1 */}
      <Section title="Production KPIs">
        <KpiGrid>
          <KpiCard label="Milk Yield" value="add in"/>
          <KpiCard label="Butterfat Percentage" value="add in"/>
          <KpiCard label="Protein Percentage" value="add in"/>
          <KpiCard label="Bulk Tank SCC" value="add in"/>
        </KpiGrid>
      </Section>
      {/* Section 2 */}
      <Section title="Feed Metric KPIs">
        <KpiGrid>
          <KpiCard label="Feed Efficiency" value="add in"/>
          <KpiCard label="Income Over Feed Cost" value="add in"/>
        </KpiGrid>
      </Section>
      {/* Section 3 */}
      <Section title="Herd Health KPIs">
        <KpiGrid>
          <KpiCard label="Subclinical Mastitis Prevalence" value="add in"/>
          <KpiCard label="Dry Period" value="add in"/>
        </KpiGrid>
      </Section> 
      {/* Section 4 */}
      <Section title="Inventory KPI">
        <KpiGrid>
          <KpiCard label="Spoilage Rate" value="add in"/>
        </KpiGrid>
      </Section>                 
      {/* Section 5 */}
      <Section title="Market and Revenue KPIs">
        <KpiGrid>
         <KpiCard label="Milk Class Prices" value="add in"/>
         <KpiCard label="Margin Per Cow" value="add in"/>
        </KpiGrid>
      </Section>
    </div>
  );
}

function Section({title, children}: any){
  return(
    <div style={{marginTop: "40px"}}>
      <h2>{title}</h2>
      {children}
    </div>
  )
}
function KpiGrid({children}: any){
  return(
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "20px",
        marginTop: "10px",
      }}
    >
      {children}
    </div>
  )
}
function KpiCard({label, value}:any) {
  return (
    <div
      style={{
        padding: "20px",
        borderRadius: "8px",
        background: "#f5f5f5",
        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
      }}
    >
      <h4>{label}</h4>
      <p style={{ fontSize: "1.5rem", marginTop: "10px"}}>{value}</p>
    </div>
  )
}
