
import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2>Knowledge AI</h2>

        <button className="new-chat-button">
          + New Chat
        </button>

        <div className="sidebar-info">
          <p>Enterprise Knowledge Assistant</p>
        </div>
      </aside>

      <main className="chat-container">
        <header className="chat-header">
          <h2>Enterprise Knowledge Assistant</h2>
          <p>Ask questions about your company documents</p>
        </header>

        <section className="chat-content">
          <div className="welcome-message">
            <h1>How can I help you today?</h1>
            <p>
              Ask me anything about your company's
              policies, working hours, leave, and more.
            </p>
          </div>
        </section>

        <form className="chat-input-container">
          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button type="submit">
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
