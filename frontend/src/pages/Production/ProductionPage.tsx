import { useEffect, useState } from "react";
import { getProductionSummary } from "../../services/api/productionService";
import AvgMilkYieldChart from "../../components/charts/production/AvgMilkYieldChart";
import SccChart from "../../components/charts/production/SccChart";
import ButterfatChart from "../../components/charts/production/ButterfatChart";
import ProteinChart from "../../components/charts/production/ProteinChart";
import PageTopbar from "../../components/layout/PageTopbar"


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
    })
  };

  const[summary, setSummary] = useState<any>(null);
  useEffect(() => {
    async function loadData() {
      try {
        const data = await getProductionSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load production summary", err);
      }
    }

    loadData();
  }, []);

  return (
    <>
      <PageTopbar 
        title="Production"
        sections={sections}
        onSelect={handleSelect}
      />
      <div style={{padding: "0px 20px 20px 40px", overflowY:"auto", height:"100%"}}>
        <Section title="Production">
          {!summary && <p>Loading...</p>}
      
          <Subsection id="milk-yield" title="Average Milk Yield Per Cow">
            {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
            <AvgMilkYieldChart data={summary.milkYieldTrend} />
            )}
          </Subsection>
      
          <Subsection id="scc" title="Bulk Tank SCC">
            {!summary ? (
                <p>No chart data loaded.</p>
              ) : (
            <SccChart data={summary.sccTrend} /> 
            )}
          </Subsection>
      
          <Subsection id="butterfat" title="Butterfat Percentage">
            {!summary ? (
                <p>No chart data loaded.</p>
              ) : (
            <ButterfatChart data={summary.butterfatTrend} />
              )}
          </Subsection>
      
          <Subsection id="protein" title="Protein Percentage">
            {!summary ? (
                  <p>No chart data loaded.</p>
                ) : (
            <ProteinChart data={summary.proteinTrend} />
            )}
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
function Subsection({id, title, children}: any){
  return(
    <div id={id} style={{marginTop: "40px",fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {title}
      {children}
    </div>
  )
}
  