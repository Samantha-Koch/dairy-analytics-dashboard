import { useEffect, useState } from "react";
import { getCostsSummary } from "../../services/api/costsService.ts";  


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
    <div>
      <h1>Costs & Revenue</h1>

      {!summary && <p>Loading...</p>}

      <h2>Costs</h2>
        <h3>Total Cost</h3>
        <h3>Feed Costs</h3>
          <h4>Total Feed Costs</h4>
          <h4>Milk to Feed Ratio</h4>
      <h2>Revenue</h2>
        <h3>Net Revenue</h3>
        <h3>Margin per Cow</h3>
        <h3>Margin per Cwt Milk</h3>

    </div>
  );
}
