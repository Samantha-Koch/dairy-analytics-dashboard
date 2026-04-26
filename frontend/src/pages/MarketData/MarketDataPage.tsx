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
      <h1>Market Data</h1>

      {!summary && <p>Loading...</p>}

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}
    </div>
  );
}
 