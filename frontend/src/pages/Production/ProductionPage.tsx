import { useEffect, useState } from "react";
import { getProductionSummary } from "../../services/api/productionService";

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
    <div>
      <h1>Production</h1>

      {!summary && <p>Loading...</p>}

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}
    </div>
  );
}

  