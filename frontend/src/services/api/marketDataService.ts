import apiClient from "./apiClient";

export async function getMarketDataSummary() {
  const response = await apiClient.get("/marketdata/summary");
  return response.data;
}
