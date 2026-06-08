import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse(null);

    const res = await fetch(
      `http://localhost:8000/ask?question=${encodeURIComponent(question)}`
    );
    const data = await res.json();
    setResponse(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "800px", margin: "40px auto", padding: "20px", fontFamily: "Arial" }}>
      
      <h1>AI SQL Assistant</h1>
      <p>Ask a question about the music database in plain English.</p>

      {/* Input area */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          placeholder="e.g. How many customers are there?"
          style={{ flex: 1, padding: "10px", fontSize: "16px", borderRadius: "6px", border: "1px solid #ccc" }}
        />
        <button
          onClick={askQuestion}
          style={{ padding: "10px 20px", fontSize: "16px", backgroundColor: "#2E5FB7", color: "white", border: "none", borderRadius: "6px", cursor: "pointer" }}
        >
          Ask
        </button>
      </div>

      {/* Loading state */}
      {loading && <p>Thinking...</p>}

      {/* Results */}
      {response && (
        <div>
          {/* SQL generated */}
          <div style={{ background: "#f4f4f2", padding: "15px", borderRadius: "6px", marginBottom: "15px" }}>
            <strong>SQL Generated:</strong>
            <pre style={{ margin: "8px 0 0", overflowX: "auto" }}>{response.sql_generated}</pre>
          </div>

          {/* Error */}
          {response.error && (
            <div style={{ background: "#FAECE7", padding: "15px", borderRadius: "6px", marginBottom: "15px", color: "#993C1D" }}>
              <strong>Error:</strong> {response.error}
            </div>
          )}

          {/* Results table */}
          {response.results && response.results.length > 0 && (
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    {Object.keys(response.results[0]).map((key) => (
                      <th key={key} style={{ padding: "10px", background: "#2E5FB7", color: "white", textAlign: "left" }}>
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {response.results.map((row, i) => (
                    <tr key={i} style={{ background: i % 2 === 0 ? "white" : "#f4f4f2" }}>
                      {Object.values(row).map((val, j) => (
                        <td key={j} style={{ padding: "10px", borderBottom: "1px solid #ddd" }}>
                          {String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              <p style={{ color: "#666", marginTop: "10px" }}>{response.results.length} rows returned</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;