
import api from "./apiClient";

export async function getDashboardSummary(customerId?: string) {
  const url = customerId
    ? `/dashboard/summary?customer_id=${customerId}`
    : `/dashboard/summary`;

  const res = await api.get(url);
  return res.data;
}
