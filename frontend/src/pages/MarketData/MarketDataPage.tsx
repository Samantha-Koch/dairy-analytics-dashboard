import { useEffect, useState } from "react";
import { getMarketDataSummary } from "../../services/api/marketDataService";
import ButterPriceChart from "../../components/charts/market/ButterPrice";
import CheesePriceChart from "../../components/charts/market/CheesePrice";
import MilkClassChart from "../../components/charts/market/MilkClass";
import MilkCompChart from "../../components/charts/market/MilkComp";
import PageTopbar from "../../components/layout/PageTopbar";

export default function MarketData() {
  const sections = [
    { id: "milk-class", label: "Milk Class Prices" },
    { id: "milk-comp", label: "Milk Composition Prices" },
    { id: "butter", label: "Butter Price" },
    { id: "cheese", label: "Cheese Price" },
  ];

  const handleSelect = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return;
  
    el.scrollIntoView({
      behavior: "smooth",
      block: "start",
    })
  };
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getMarketDataSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load costs summary", err);
      }
    }

    loadData();
  }, []);


  return (
    <>
      <PageTopbar 
        title="Costs & Revenue"
        sections={sections}
        onSelect={handleSelect}
      />
      <div style={{padding: "0px 20px 20px 40px", overflowY:"auto", height:"100%"}}>
        <Section title="Market Trends">
          {!summary && <p>Loading...</p>}
      
          <Subsection id="milk-class" title="Milk Class Prices">
            {!summary ? (
              <p>No chart data loaded.</p>
            ) : (
            <MilkClassChart data={summary.milkClassTrend} />
            )}
          </Subsection>
      
          <Subsection id="milk-comp" title="Milk Component Prices">
            {!summary ? (
                <p>No chart data loaded.</p>
              ) : (
            <MilkCompChart data={summary.milkCompTrend} /> 
            )}
          </Subsection>
      
          <Subsection id="butter" title="Butter Price">
            {!summary ? (
                <p>No chart data loaded.</p>
              ) : (
            <ButterPriceChart data={summary.butterPriceTrend} />
              )}
          </Subsection>
      
          <Subsection id="cheese" title="Cheese Price">
            {!summary ? (
                  <p>No chart data loaded.</p>
                ) : (
            <CheesePriceChart data={summary.cheesePriceTrend} />
            )}
          </Subsection>
        </Section>
      </div>
    </>  
  );
  
}
function Section({title, children}: any){
  return(
    <div style={{marginTop: "40px", fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {title}
      {children}
    </div>
  )
}
function Subsection({id, title, children}: any){
  return(
    <div id={id} style={{marginTop: "40px", fontFamily: "helvetica neue",fontSize: "14pt"}}>
      {title}
      {children}
    </div>
  )
}

 