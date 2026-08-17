"use client";
import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [ques, setQuestion] = useState("");
  const [err, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [ans, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await fetch("http://localhost:8000/ingest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        repo_url: url,
      }),
    });

    if (!res.ok) {
      setError("Internal Server Error");
      setLoading(false);
      return;
    }

    const result = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: ques,
      }),
    });

    if (!result.ok) {
      setError("Internal Server Error");
      setLoading(false);
      return;
    }
    const data = await result.json();
    setAnswer(data.answer);
    setSources(data.sources);
    setLoading(false);
  }
  return (
    <div className="main">
      <h1>Ask My Repo</h1>
      <p>Paste your url and Ask any questions from your repo</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="repo-url"
          id="repo-url"
          value={url}
          placeholder="Paste repo url"
          onChange={(e) => setUrl(e.target.value)}
        />
        <input
          type="text"
          name="question"
          id="question"
          placeholder="What's your question?"
          value={ques}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit">Get Answer</button>
      </form>
      {loading && (!err || !ans) && <div className="loading">Loading...</div>}
      {err && (
        <div className="err">
          <p>{err} </p>
        </div>
      )}
      {ans && (
        <div className="solution">
          <p>Your Answer:</p>
          <p>{ans}</p>
          <p>Sources files cited:</p>
          <ul>
            {sources.map((src) => (
              <li key={src}>{src}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
