
const API_BASE_URL = "http://localhost:8000";

export interface ChatResponse {
  question: string;
  answer: string;
  has_evidence: boolean;
}

export async function sendQuestion(
  question: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Unable to get a response from the assistant.");
  }

  return response.json();
}
