import { useEffect, useState } from "react";
import { getCostsSummary } from "../../services/api/costsService.ts";  

import MarginCowChart from "../../components/charts/costs/MarginCow";
import MarginCwtChart from "../../components/charts/costs/MarginCwt";
import MilkFeedRatioChart from "../../components/charts/costs/MilkFeedRatio";
import NetRevenueChart from "../../components/charts/costs/NetRevenue";
import TotalCostsChart from "../../components/charts/costs/TotalCosts";
import TotalFeedCostsChart from "../../components/charts/costs/TotalFeedCosts";

export default function Costs() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getCostsSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load costs summary", err);
      }
    }

    loadData();
  }, []);


  return (
    <Section title="Costs & Revenue">
      {!summary && <p>Loading...</p>}
      <SubTitle title="Costs"></SubTitle>
      <Subsection title="Total Costs">
        {!summary ? (
          <p>No chart data loaded.</p>
        ) : (
        <TotalCostsChart data={summary.totalCostsTrend} />
        )}
      </Subsection>

      <SubGroup title="Feed Trends"></SubGroup>
      <Subsection title="Total Feed Costs">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <TotalFeedCostsChart data={summary.totalFeedCostsTrend} /> 
        )}
      </Subsection>
  
      <Subsection title="Milk to Feed Ratio">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <MilkFeedRatioChart data={summary.milkFeedRatioTrend} />
          )}
      </Subsection>
  
      <SubTitle title="Revenue"></SubTitle>
      <Subsection title="Net Revenue">
        {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
        <NetRevenueChart data={summary.netRevenueTrend} />
        )}
      </Subsection>
      <Subsection title="Margin per Cow">
        {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
        <MarginCowChart data={summary.marginCowTrend} />
        )}
      </Subsection>
      <Subsection title="Margin per CWT of Milk">
        {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
        <MarginCwtChart data={summary.marginCwtTrend} />
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
      <h4>{title}</h4>
      {children}
    </div>
  )
}
function SubGroup({title, children}: any){
  return(
    <div style={{marginTop: "40px"}}>
      <h3>{title}</h3>
      {children}
    </div>
  )
}
function SubTitle({title, children}: any){
  return(
    <div style={{marginTop: "40px"}}>
      <h2>{title}</h2>
      {children}
    </div>
  )
}

