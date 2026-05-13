import { useState } from "react";
import { uploadDataFile } from "../../services/api/dataUploadService";

export default function DataUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [customerId, setCustomerId] = useState("");   // NEW
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    console.log("UPLOAD CLICKED");
    if (!file || !customerId) {
      setMessage("Please provide both a file and a Customer ID.");
      return;
    }

    try {
      const result = await uploadDataFile(file, customerId);   // UPDATED
      setMessage(result.message || "Upload successful");
    } catch (err) {
      setMessage("Upload failed");
      console.error(err);
    }
  };

  return (
    <Section title="Upload Your Data">
      <div
        style={{
          padding: "20px",
          fontFamily: "helvetica neue",
          overflowY: "auto",
          height: "100%",
        }}
      >

        {/* NEW CUSTOMER ID FIELD */}
        <input
          type="text"
          placeholder="Customer ID (email address)"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          style={{
            marginBottom: "10px",
            padding: "8px",
            width: "250px",
            fontFamily: "helvetica neue",
            fontSize: "14px",
            display: "block",
          }}
        />

        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <button
          onClick={handleUpload}
          disabled={!file || !customerId}
          style={{
            marginTop: "10px",
            padding: "8px 16px",
            cursor: file && customerId ? "pointer" : "not-allowed",
            fontFamily: "helvetica neue",
            fontSize: "14px",
          }}
        >
          Upload
        </button>

        {message && (
          <p
            style={{
              marginTop: "10px",
              fontFamily: "helvetica neue",
              fontSize: "12pt",
            }}
          >
            {message}
          </p>
        )}
      </div>
    </Section>
  );
}

function Section({ title, children }: any) {
  return (
    <div
      style={{
        marginTop: "5%",
        padding: "20px",
        fontFamily: "helvetica neue",
        fontSize: "20pt",
      }}
    >
      {title}
      {children}
    </div>
  );
}
