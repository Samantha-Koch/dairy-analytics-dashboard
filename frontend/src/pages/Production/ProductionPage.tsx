import { useEffect, useState } from "react";
import { getProductionSummary } from "../../services/api/productionService";
import AvgMilkYieldChart from "../../components/charts/production/AvgMilkYieldChart";
import SccChart from "../../components/charts/production/SccChart";
import ButterfatChart from "../../components/charts/production/ButterfatChart";
import ProteinChart from "../../components/charts/production/ProteinChart";


export default function Production() {
  const [summary, setSummary] = useState<any>(null);

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
    <Section title="Production">
      {!summary && <p>Loading...</p>}
  
      <Subsection title="Average Milk Yield Per Cow">
        {!summary ? (
          <p>No chart data loaded.</p>
        ) : (
        <AvgMilkYieldChart data={summary.milkYieldTrend} />
        )}
      </Subsection>
  
      <Subsection title="Bulk Tank SCC">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <SccChart data={summary.sccTrend} /> 
        )}
      </Subsection>
  
      <Subsection title="Butterfat Percentage">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <ButterfatChart data={summary.butterfatTrend} />
          )}
      </Subsection>
  
      <Subsection title="Protein Percentage">
        {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
        <ProteinChart data={summary.proteinTrend} />
        )}
      </Subsection>
    </Section>
  );
  
}
function Section({title, children}: any){
  return(
    <div style={{marginTop: "40px"}}>
      <h1>{title}</h1>
      {children}
    </div>
  )
}
function Subsection({title, children}: any){
  return(
    <div style={{marginTop: "40px"}}>
      <h2>{title}</h2>
      {children}
    </div>
  )
}
  