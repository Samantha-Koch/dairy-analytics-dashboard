import { useState } from "react";
import { uploadDataFile } from "../../services/api/dataUploadService";

export default function DataUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    try {
      const result = await uploadDataFile(file);
      setMessage(result.message);
    } catch (err) {
      setMessage("Upload failed");
      console.error(err);
    }
  };

  return (
    <Section title="Upload Your Data">
    <div style={{ padding: "20px",fontFamily: "helvetica neue", overflowY:"auto", height:"100%"}}>

      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button
        onClick={handleUpload}
        disabled={!file}
        style={{
          marginTop: "10px",
          padding: "8px 16px",
          cursor: file ? "pointer" : "not-allowed",
          fontFamily: "helvetica neue",
          fontSize: "14px",
        }}
      >
        Upload
      </button>

      {message && <p style={{ marginTop: "10px",fontFamily: "helvetica neue",fontSize: "12pt"}}>{message}</p>}
    </div>
    </Section>
  )
}
function Section({title, children}: any){
  return(
    <div style={{marginTop: "5%",padding: "20px",fontFamily: "helvetica neue",fontSize: "20pt"}}>
      {title}
      {children}
    </div>
  )
}