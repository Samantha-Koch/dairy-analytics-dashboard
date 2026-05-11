import apiClient from "./apiClient";


export const getMilkClassPrices = async (year: string | number = "all") => {
  const response = await apiClient.get("/marketdata/milk_class_prices", {
    params: { year }
  });
  return response.data;
};

export const getMilkCompPrices = async (year: string | number = "all") => {
  const response = await apiClient.get("/marketdata/milk_comp_prices", {
    params: { year }
  });
  return response.data;
};

export const getButterPrices = async (year: string | number = "all") => {
  const response = await apiClient.get("/marketdata/butter_prices", {
    params: { year }
  });
  return response.data;
};

export const getCheesePrices = async (year: string | number = "all") => {
  const response = await apiClient.get("/marketdata/cheese_prices", {
    params: { year }
  });
  return response.data;
};
