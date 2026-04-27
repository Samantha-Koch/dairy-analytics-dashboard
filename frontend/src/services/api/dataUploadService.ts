import apiClient from "./apiClient";

export async function getDataUploadSummary() {
  const response = await apiClient.get("/dataupload/summary");
  return response.data;
}
