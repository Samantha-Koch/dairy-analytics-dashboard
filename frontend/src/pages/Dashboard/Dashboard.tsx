import { useEffect, useState } from "react";
import { getDashboardSummary } from "../../services/api/dashboardService";
import PageTopbar from "../../components/layout/PageTopbar"

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const sections = [
    { id: "production-KPI", label: "Production KPIs" },
    { id: "feed-KPI", label: "Feed Metric KPIs" },
    { id: "health-KPI", label: "Herd Health KPIs" },
    { id: "inventory-KPI", label: "Inventory KPIs" },
    { id: "market-KPI", label: "Market and Revnue KPIs" },
  ];

  const handleSelect = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return;
  
    el.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };
  

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
    <>
      <PageTopbar 
        title="Dairy Analytics Dashboard"
        sections={sections}
        onSelect={handleSelect}
      />
      <div style={{padding: "0px 20px 20px 40px", overflowY:"auto", height:"100%"}}>
          <PageTitle title="Dairy Analytics Dashboard">    
          {/* Section 1 */}
          <Section id="production-KPI" title="Production KPIs">
            <KpiGrid>
              <KpiCard label="Milk Yield" value="add in"/>
              <KpiCard label="Butterfat Percentage" value="add in"/>
              <KpiCard label="Protein Percentage" value="add in"/>
              <KpiCard label="Bulk Tank SCC" value="add in"/>
            </KpiGrid>
          </Section>
          {/* Section 2 */}
          <Section id="feed-KPI" title="Feed Metric KPIs">
            <KpiGrid>
              <KpiCard label="Feed Efficiency" value="add in"/>
              <KpiCard label="Income Over Feed Cost" value="add in"/>
            </KpiGrid>
          </Section>
          {/* Section 3 */}
          <Section id="health-KPI" title="Herd Health KPIs">
            <KpiGrid>
              <KpiCard label="Subclinical Mastitis Prevalence" value="add in"/>
              <KpiCard label="Dry Period" value="add in"/>
            </KpiGrid>
          </Section> 
          {/* Section 4 */}
          <Section id="inventory-KPI" title="Inventory KPI">
            <KpiGrid>
              <KpiCard label="Spoilage Rate" value="add in"/>
            </KpiGrid>
          </Section>                 
          {/* Section 5 */}
          <Section id="market-KPI" title="Market and Revenue KPIs">
            <KpiGrid>
            <KpiCard label="Milk Class Prices" value="add in"/>
            <KpiCard label="Margin Per Cow" value="add in"/>
            </KpiGrid>
          </Section>
          </PageTitle>
      </div>
    </>    
  );
}

function Section({id, title, children}: any){
  return(
    <div id={id} style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "14pt"}}>
      {title}
      {children}
    </div>
  )
}
function PageTitle({title, children}: any){
  return(
    <div style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {title}
      {children}
    </div>
  )
}
function KpiGrid({children}: any){
  return(
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
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
        fontFamily: "helvetica neue",
        fontSize: "12pt",
      }}
    >
      {label}
      <p style={{marginTop: "10px",fontFamily: "helvetica neue",fontSize: "12pt"}}>{value}</p>
    </div>
  )
}
