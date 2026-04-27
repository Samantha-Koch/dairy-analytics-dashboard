import apiClient from "./apiClient";

export async function uploadDataFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/dataupload/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });

  return response.data;
}
