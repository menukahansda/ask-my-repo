"use client";

interface Props {
  url: string;
  setUrl: (v: string) => void;
  question: string;
  setQuestion: (v: string) => void;
  onSubmit: (e: React.SubmitEvent<HTMLFormElement>) => void;
  loading: boolean;
  error: string;
  answer: string;
  sources: string[];
}

export default function RepoOnboarding({
  url,
  setUrl,
  question,
  setQuestion,
  onSubmit,
  loading,
  error,
  answer,
  sources,
}: Props) {
  return (
    <>
      <div>
        <h1 className="prompt-line">
          <span className="prompt-symbol">$</span> ask-my-repo
          <span className="cursor" />
        </h1>
        <p className="term-sub">point me at a repo, then ask anything.</p>
      </div>

      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <label className="field">
          <span className="field-label">
            <span className="field-arrow">→</span> repo url
          </span>
          <input
            type="text"
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
            value={question}
            placeholder="where's the auth logic handled?"
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

      {error && (
        <div className="err-box">
          <span className="err-symbol">✕</span> {error}
        </div>
      )}

      {answer && (
        <div className="flex flex-col gap-4">
          <div className="answer-box">
            <div className="answer-label">output</div>
            <p className="answer-text">{answer}</p>
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
    </>
  );
}