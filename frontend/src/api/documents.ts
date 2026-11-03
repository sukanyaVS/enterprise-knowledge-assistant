const API_BASE_URL = "http://localhost:8000";

export interface UploadResponse {
  message: string;
  filename: string;
  chunks_processed: number;
  previous_chunks_replaced: number;
  total_chunks_in_database: number;
}

export async function uploadDocument(
  file: File
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.detail || "Document upload failed."
    );
  }

  return response.json();
}