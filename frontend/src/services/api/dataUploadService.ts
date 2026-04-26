import apiClient from "./apiClient";

export async function getDataUploadSummary() {
  const response = await apiClient.get("/data-upload/summary");
  return response.data;
}
