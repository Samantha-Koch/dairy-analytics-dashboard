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
      <h1>Costs</h1>

      {!summary && <p>Loading...</p>}

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}
    </div>
  );
}
