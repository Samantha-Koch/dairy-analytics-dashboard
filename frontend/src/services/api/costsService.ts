import apiClient from "./apiClient";

export async function getCostsSummary() {
  const response = await apiClient.get("/costs/summary");
  return response.data;
}
