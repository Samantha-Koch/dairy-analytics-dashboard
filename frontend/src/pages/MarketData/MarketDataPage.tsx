import { useEffect, useState } from "react";
import { getMarketDataSummary } from "../../services/api/marketDataService";

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
    <div>
      <h1>Market Trends</h1>

      {!summary && <p>Loading...</p>}

      <h2>Milk Class Prices</h2>
      <h2>Milk Component Prices</h2>
      <h2>Butter Price</h2>
      <h2>Cheese Price</h2>
      
    </div>
  );
}
 