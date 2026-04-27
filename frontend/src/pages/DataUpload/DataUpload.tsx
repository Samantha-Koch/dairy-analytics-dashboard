import { useState } from "react";
import { uploadDataFile } from "../../services/api/dataUploadService";

export default function DataUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    try {
      const result = await uploadDataFile(file);
      setMessage(`Uploaded: ${result.filename}`);
    } catch (err) {
      setMessage("Upload failed");
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Upload Your Data</h1>

      <input
        type="file"
        accept=".csv,.xlsx,.xls,.json"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button
        onClick={handleUpload}
        disabled={!file}
        style={{
          marginTop: "10px",
          padding: "8px 16px",
          cursor: file ? "pointer" : "not-allowed"
        }}
      >
        Upload
      </button>

      {message && <p style={{ marginTop: "10px" }}>{message}</p>}
    </div>
  );
}
