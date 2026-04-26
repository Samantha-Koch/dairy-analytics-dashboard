import { useEffect, useState } from "react";
import { getDashboardSummary } from "../../services/api/dashboardService";
import React from "react";

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load dashboard summary", err);
      }
    }

    loadData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>

      {!summary && <p>Loading...</p>}

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}
    </div>
  );
}
