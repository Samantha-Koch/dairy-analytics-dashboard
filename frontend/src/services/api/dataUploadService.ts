import apiClient from "./apiClient";

export async function uploadDataFile(file: File, customerId: string) {
  console.log("SERVICE CALLED", file, customerId);
  const formData = new FormData();
  formData.append("file", file);
  formData.append("customer_id", customerId);

  const response = await apiClient.post("/dataupload/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });

  console.log("RESPONSE RECEIVED", response);
  return response.data;
}
