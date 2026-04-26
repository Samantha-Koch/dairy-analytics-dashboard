import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000", // adjust if your backend uses a different port
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
