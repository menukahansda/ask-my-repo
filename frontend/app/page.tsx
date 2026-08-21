"use client";
import { useState, useEffect } from "react";
import RepoOnboarding from "./components/RepoOnboarding";

export default function Home() {
  const [url, setUrl] = useState("");
  const [ques, setQuestion] = useState("");
  const [err, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [ans, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetch(`${API_URL}/`).catch(() => {});
  }, []);

  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setAnswer("");
    setSources([]);
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
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

      const ingestData = await res.json();

      const result = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: ques,
          repo_slug: ingestData.repo_slug,
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
            <RepoOnboarding
              url={url}
              setUrl={setUrl}
              question={ques}
              setQuestion={setQuestion}
              onSubmit={handleSubmit}
              loading={loading}
              error={err}
              answer={ans}
              sources={sources}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
