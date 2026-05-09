import { useEffect, useState } from "react";
import { getDashboardSummary } from "../../services/api/dashboardService";
import PageTopbar from "../../components/layout/PageTopbar"
import KpiCard from "../../components/kpi_cards/KpiCard"

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
              <KpiCard title="Milk Yield" data={summary.milk_yield}/>
              <KpiCard title="Butterfat Percentage" data={summary.butterfat_percent}/>
              <KpiCard title="Protein Percentage" data={summary.protein_percent}/>
              <KpiCard title="Bulk Tank SCC" data={summary.bulk_scc}/>
            </KpiGrid>
          </Section>
          {/* Section 2 */}
          <Section id="feed-KPI" title="Feed Metric KPIs">
            <KpiGrid>
              <KpiCard title="Feed Efficiency" data={summary.feed_efficiency}/>
              <KpiCard title="Income Over Feed Cost" data={summary.income_over_feed}/>
            </KpiGrid>
          </Section>
          {/* Section 3 */}
          <Section id="health-KPI" title="Herd Health KPIs">
            <KpiGrid>
              <KpiCard title="Subclinical Mastitis Prevalence" data={summary.mastitis_prev}/>
              <KpiCard title="Dry Period" data={summary.dry_period}/>
            </KpiGrid>
          </Section> 
          {/* Section 4 */}
          <Section id="inventory-KPI" title="Inventory KPI">
            <KpiGrid>
              <KpiCard title="Spoilage Rate" data={summary.spoilage_rate}/>
            </KpiGrid>
          </Section>                 
          {/* Section 5 */}
          <Section id="market-KPI" title="Market and Revenue KPIs">
            <KpiGrid>
            <KpiCard title="Milk Class Prices" data={summary.milk_class}/>
            <KpiCard title="Margin Per Cow" data={summary.margin_per_cow}/>
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

