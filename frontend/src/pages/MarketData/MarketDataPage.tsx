import { useEffect, useState } from "react";
import { getMarketDataSummary } from "../../services/api/marketDataService";
import ButterPriceChart from "../../components/charts/market/ButterPrice";
import CheesePriceChart from "../../components/charts/market/CheesePrice";
import MilkClassChart from "../../components/charts/market/MilkClass";
import MilkCompChart from "../../components/charts/market/MilkComp";

export default function MarketData() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getMarketDataSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load market data summary", err);
      }
    }

    loadData();
  }, []);

  return (
    <Section title="Market Trends">
      {!summary && <p>Loading...</p>}
  
      <Subsection title="Milk Class Prices">
        {!summary ? (
          <p>No chart data loaded.</p>
        ) : (
        <MilkClassChart data={summary.milkClassTrend} />
        )}
      </Subsection>
  
      <Subsection title="Milk Component Prices">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <MilkCompChart data={summary.milkCompTrend} /> 
        )}
      </Subsection>
  
      <Subsection title="Butter Price">
        {!summary ? (
            <p>No chart data loaded.</p>
          ) : (
        <ButterPriceChart data={summary.butterPriceTrend} />
          )}
      </Subsection>
  
      <Subsection title="Cheese Price">
        {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
        <CheesePriceChart data={summary.cheesePriceTrend} />
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

 