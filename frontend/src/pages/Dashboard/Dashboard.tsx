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
  return (
    <div style={{padding: "20px"}}>
      <h1>Dairy Analytics Dashboard</h1>
      
      {/* Section 1 */}
      <Section title="Production KPIs">
        <KpiGrid>
          <div className="kpi-card">
            <h3>Milk Per Cow</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Butterfat Percentage</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Protein Percentage</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Bulk Tank SCC</h3>
            /* link kpi data here */
          </div>
        </KpiGrid>
      </Section>
      {/* Section 2 */}
      <Section title="Feed Metric KPIs">
        <KpiGrid>
          <div className="kpi-card">
            <h3>Feed Efficiency</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Income Over Feed Cost</h3>
            /* link kpi data here */
          </div>
        </KpiGrid>
      </Section>
      {/* Section 3 */}
      <Section title="Herd Health KPIs">
        <KpiGrid>
          <div className="kpi-card">
            <h3>Subclinical Mastitis Prevalence</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Dry Period</h3>
            /* link kpi data here */
          </div>
        </KpiGrid>
      </Section> 
      {/* Section 4 */}
      <Section title="Inventory KPI">
        <KpiGrid>
          <div className="kpi-card">
            <h3>Spoilage Rate</h3>
            /* link kpi data here */
          </div>
        </KpiGrid>
      </Section>                 
      {/* Section 5 */}
      <Section title="Market and Revenue KPIs">
        <KpiGrid>
          <div className="kpi-card">
            <h3>Milk Class Prices</h3>
            /* link kpi data here */
          </div>
          <div className="kpi-card">
            <h3>Margin Per Cow</h3>
            /* link kpi data here */
          </div>
        </KpiGrid>
      </Section>
      {/* RAW JSON */}
      <pre style={{marginTop: "40px"}}>
        {JSON.stringify(summary, null, 2)}
      </pre>
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
