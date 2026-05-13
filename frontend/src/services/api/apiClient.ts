import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api/v1", // adjust if your backend uses a different port
});

export default apiClient;
