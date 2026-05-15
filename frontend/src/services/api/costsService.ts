import apiClient from "./apiClient";

export type CostsSource = "usda" | "customer" | "both";
export type CostsFrequency = "annual" | "monthly";

interface CostsQueryParams {
  source: CostsSource;
  frequency: CostsFrequency;
  year?: string;
  customerId?: string;
}

export const getTotalCostsData = async (params: CostsQueryParams) => {
  const response = await apiClient.get("/costs/total_costs", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getTotalCostsAvailableYears = async () => {
  const response = await apiClient.get("/costs/total_costs/available_years");
  return response.data; // { years: number[] }
};


export const getTotalFeedCostsData = async (params: CostsQueryParams) => {
  const response = await apiClient.get("/costs/total_feed_costs", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getTotalFeedCostsAvailableYears = async () => {
  const response = await apiClient.get("/costs/total_feed_costs/available_years");
  return response.data;
};


export const getMilkFeedRatioData = async (params: CostsQueryParams) => {
  const response = await apiClient.get("/costs/milk_feed_ratio", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getMilkFeedRatioAvailableYears = async () => {
  const response = await apiClient.get("/costs/milk_feed_ratio/available_years");
  return response.data;
};


export const getNetRevenueData = async (params: CostsQueryParams) => {
  const response = await apiClient.get("/costs/net_revenue", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getNetRevenueAvailableYears = async () => {
  const response = await apiClient.get("/costs/net_revenue/available_years");
  return response.data;
};


export const getMarginPerCowData = async (params: CostsQueryParams) => {
  const response = await apiClient.get("/costs/margin_per_cow", {
    params: {
      source: params.source,
      frequency: params.frequency,
      ...(params.frequency === "monthly" && params.year ? { year: params.year } : {}),
      ...(params.customerId ? { customer_id: params.customerId } : {}),
    },
  });
  return response.data;
};

export const getMarginPerCowAvailableYears = async () => {
  const response = await apiClient.get("/costs/margin_per_cow/available_years");
  return response.data;
};
