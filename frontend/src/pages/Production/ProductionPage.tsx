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
      <h2>Milk Yield Per Cow</h2>
      <h2>Bulk Tank SCC</h2>
      <h2>Butterfat Percentage</h2>
      <h2>Protein Percentage</h2>
    </div>
  );
}

  