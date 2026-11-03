
import { useState } from "react";
import { sendQuestion } from "./api/chat";
import type { SourceReference } from "./api/chat";
import type { ChatResponse } from "./api/chat";
import "./App.css";
import { uploadDocument } from "./api/documents";

interface Message {
  role: "user" | "assistant";
  content: string;
  hasEvidence?: boolean;
  sources?: SourceReference[];
}

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const userQuestion = question.trim();

    if (!userQuestion || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);
    setError("");

    try {
      const result: ChatResponse = await sendQuestion(userQuestion);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          hasEvidence: result.has_evidence,
          sources: result.sources,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (
  event: React.ChangeEvent<HTMLInputElement>
) => {
  const file = event.target.files?.[0];

  if (!file) return;

  setUploading(true);
  setUploadMessage("");
  setUploadError("");

  try {
    const result = await uploadDocument(file);

    setUploadMessage(
      `${result.filename} uploaded successfully. ${result.chunks_processed} chunks processed.`
    );
  } catch (error) {
    setUploadError(
      error instanceof Error
        ? error.message
        : "Document upload failed."
    );
  } finally {
    setUploading(false);
    event.target.value = "";
  }
};

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2>Knowledge AI</h2>

        <button
          className="new-chat-button"
          onClick={() => {
            setMessages([]);
            setError("");
          }}
        >
          + New Chat
        </button>

        <div className="sidebar-info">
          <p>Enterprise Knowledge Assistant</p>
        </div>

        <div className="document-upload">
          <label htmlFor="document-upload">
            {uploading ? "Uploading..." : "Upload Document"}
          </label>

          <input
            id="document-upload"
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileUpload}
            disabled={uploading}
          />

          {uploadMessage && <p className="upload-success">{uploadMessage}</p>}

          {uploadError && <p className="upload-error">{uploadError}</p>}
        </div>
      </aside>

      <main className="chat-container">
        <header className="chat-header">
          <h2>Enterprise Knowledge Assistant</h2>
          <p>Ask questions about your company documents</p>
        </header>

        <section className="chat-content">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h1>How can I help you today?</h1>
              <p>
                Ask me anything about your company's policies, working hours,
                leave, and more.
              </p>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  <strong>
                    {message.role === "user" ? "You" : "Assistant"}
                  </strong>

                  <p>{message.content}</p>

                  {message.role === "assistant" &&
                    message.sources &&
                    message.sources.length > 0 && (
                      <div className="message-sources">
                        <strong>Sources</strong>

                        {message.sources.map((source, sourceIndex) => (
                          <div
                            key={`${source.filename}-${source.page ?? "none"}-${sourceIndex}`}
                            className="source-item"
                          >
                            <span>{source.filename}</span>

                            {source.page !== null && (
                              <span> — Page {source.page}</span>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                  {message.role === "assistant" &&
                    message.hasEvidence === false && (
                      <small>Information not found in documents</small>
                    )}
                </div>
              ))}

              {loading && (
                <div className="message assistant">
                  <strong>Assistant</strong>
                  <p>Searching documents and preparing an answer...</p>
                </div>
              )}
            </div>
          )}
        </section>

        {error && <p className="error-message">{error}</p>}

        <form className="chat-input-container" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading || !question.trim()}>
            {loading ? "Sending..." : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
