import apiClient from "./apiClient";

export async function getProductionSummary() {
  const response = await apiClient.get("/production/summary");
  return response.data;
}
