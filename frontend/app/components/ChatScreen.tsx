"use client";
import type { Message } from "../page";

interface Props {
  repoSlug: string;
  question: string;
  setQuestion: (v: string) => void;
  onSubmit: (e: React.SubmitEvent<HTMLFormElement>) => void;
  onNewRepo: () => void;
  loading: boolean;
  error: string;
  messages: Message[];
}

export default function ChatScreen({
  repoSlug,
  question,
  setQuestion,
  onSubmit,
  onNewRepo,
  loading,
  error,
  messages,
}: Props) {
  return (
    <>
      <div>
        <h1 className="prompt-line">
          <span className="prompt-symbol">$</span> ask-my-repo
          <span className="cursor" />
        </h1>
        <p className="term-sub">chatting with {repoSlug}</p>
      </div>

      <div className="flex flex-col gap-4 max-h-[50vh] overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className="flex flex-col gap-2">
            <div className="prompt-line">
              <span className="prompt-symbol">?</span> {msg.question}
            </div>
            <div className="answer-box">
              <div className="answer-label">output</div>
              <p className="answer-text">{msg.answer}</p>
            </div>
            {msg.sources.length > 0 && (
              <div className="diff-box">
                <div className="answer-label">sources cited</div>
                <ul className="diff-list">
                  {msg.sources.map((src) => (
                    <li key={src} className="diff-line">
                      <span className="diff-plus">+</span> {src}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={onSubmit} className="flex flex-col gap-4">
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

        <div className="flex gap-2">
          <button type="submit" className="run-btn" disabled={loading}>
            {loading ? "running…" : "run query"}
          </button>
          <button type="button" onClick={onNewRepo} className="run-btn">
            new repo
          </button>
        </div>
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
    </>
  );
}
