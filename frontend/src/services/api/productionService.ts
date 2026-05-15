import apiClient from "./apiClient";

export type ProductionSource = "usda" | "customer" | "both";
export type ProductionFrequency = "annual" | "monthly";

interface ProductionQueryParams {
  source: ProductionSource;
  frequency: ProductionFrequency;
  year?: string;
  customerId?: string;
}

export const getMilkYieldData = async (params: ProductionQueryParams) => {
  const response = await apiClient.get("/production/milk_yield", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getSccData = async (params: ProductionQueryParams) => {
  const response = await apiClient.get("/production/scc", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getButterfatData = async (params: ProductionQueryParams) => {
  const response = await apiClient.get("/production/butterfat", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getProteinData = async (params: ProductionQueryParams) => {
  const response = await apiClient.get("/production/protein", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getAvailableYears = async (metric: "milk_yield" | "scc" | "butterfat" | "protein") => {
  const response = await apiClient.get(`/production/${metric}/available_years`);
  return response.data; // { years: number[] }
};
