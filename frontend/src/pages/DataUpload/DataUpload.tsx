import { useEffect, useState } from "react";
import { getDataUploadSummary } from "../../services/api/dataUploadService";

export default function DataUpload() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getDataUploadSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to load data upload summary", err);
      }
    }

    loadData();
  }, []);

  return (
    <div>
      <h1>Data Upload</h1>

      {!summary && <p>Loading...</p>}

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}
    </div>
  );
}
