import apiClient from "./apiClient";

export async function getMarketDataSummary() {
  const response = await apiClient.get("/market-data/summary");
  return response.data;
}
