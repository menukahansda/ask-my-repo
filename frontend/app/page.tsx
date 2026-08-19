"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [ques, setQuestion] = useState("");
  const [err, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [ans, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const REINDEX_TOKEN = process.env.NEXT_PUBLIC_REINDEX_TOKEN || "";

  useEffect(() => {
    fetch(`${API_URL}/`).catch(() => {});
  }, []);

  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-reindex-token": REINDEX_TOKEN,
        },
        body: JSON.stringify({
          repo_url: url,
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        setError(body?.message || "Internal Server Error");
        return;
      }

      const result = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: ques,
        }),
      });

      if (!result.ok) {
        const body = await result.json().catch(() => null);
        setError(body?.message || "Internal Server Error");
        return;
      }
      const data = await result.json();
      setAnswer(data.answer);
      setSources(data.sources);
    } catch {
      setError("Could not reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 term-bg">
      <div className="w-full max-w-2xl flex flex-col gap-4">
        <div className="term-window">
          <div className="flex items-center gap-2 px-4 py-3 term-titlebar">
            <span className="dot dot-red" />
            <span className="dot dot-yellow" />
            <span className="dot dot-green" />
            <span className="term-title">ask-my-repo — zsh</span>
          </div>

          <div className="px-6 py-8 flex flex-col gap-6">
            <div>
              <h1 className="prompt-line">
                <span className="prompt-symbol">$</span> ask-my-repo
                <span className="cursor" />
              </h1>
              <p className="term-sub">point me at a repo, then ask anything.</p>
            </div>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <label className="field">
                <span className="field-label">
                  <span className="field-arrow">→</span> repo url
                </span>
                <input
                  type="text"
                  name="repo-url"
                  id="repo-url"
                  value={url}
                  placeholder="github.com/you/your-repo"
                  onChange={(e) => setUrl(e.target.value)}
                  className="field-input"
                  required
                />
              </label>

              <label className="field">
                <span className="field-label">
                  <span className="field-arrow">?</span> question
                </span>
                <input
                  type="text"
                  name="question"
                  id="question"
                  placeholder="where's the auth logic handled?"
                  value={ques}
                  onChange={(e) => setQuestion(e.target.value)}
                  className="field-input"
                  required
                />
              </label>

              <button type="submit" className="run-btn" disabled={loading}>
                {loading ? "running…" : "run query"}
              </button>
            </form>

            {loading && (
              <div className="thinking">
                <span className="thinking-dot" />
                <span className="thinking-dot" />
                <span className="thinking-dot" />
                <span className="term-sub">reading the codebase…</span>
              </div>
            )}

            {err && (
              <div className="err-box">
                <span className="err-symbol">✕</span> {err}
              </div>
            )}

            {ans && (
              <div className="flex flex-col gap-4">
                <div className="answer-box">
                  <div className="answer-label">output</div>
                  <p className="answer-text">{ans}</p>
                </div>

                {sources.length > 0 && (
                  <div className="diff-box">
                    <div className="answer-label">sources cited</div>
                    <ul className="diff-list">
                      {sources.map((src) => (
                        <li key={src} className="diff-line">
                          <span className="diff-plus">+</span> {src}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
