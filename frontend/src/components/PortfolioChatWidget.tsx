import {
  Bot,
  ExternalLink,
  LoaderCircle,
  MessageCircle,
  Send,
  Sparkles,
  X,
} from "lucide-react";
import {
  type FormEvent,
  useEffect,
  useRef,
  useState,
} from "react";

import {
  getVisitorKey,
} from "../hooks/useAnalyticsTracker";
import {
  publicApi,
  resolveApiUrl,
} from "../lib/api";
import type {
  ChatHistoryMessage,
  ChatSource,
} from "../types/ai";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
  grounded?: boolean;
  answerMode?: "portfolio" | "general" | "mixed";
}

const fallbackSuggestions = [
  "What are Bajirao's strongest technical skills?",
  "Explain the RecruitAI Pro project.",
  "What was the result of his NLP research?",
  "Is he suitable for a Python backend role?",
];

function createMessageId(): string {
  if (
    typeof crypto !== "undefined" &&
    typeof crypto.randomUUID === "function"
  ) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random()}`;
}

function resolveSourceUrl(
  sourceUrl: string | null,
): string | null {
  if (!sourceUrl) {
    return null;
  }

  if (
    sourceUrl.startsWith("/api/") ||
    sourceUrl.startsWith("/media/")
  ) {
    return resolveApiUrl(sourceUrl);
  }

  return sourceUrl;
}

export default function PortfolioChatWidget() {
  const [open, setOpen] =
    useState(false);

  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [suggestions, setSuggestions] =
    useState<string[]>(
      fallbackSuggestions,
    );

  const [messages, setMessages] =
    useState<ChatMessage[]>([
      {
        id: "welcome",
        role: "assistant",
        content:
          "Hello. I am Bajirao AI Assistant. Ask me about Bajirao's portfolio, projects and skills, or ask general questions about coding, AI/ML, interviews and technology.",
        grounded: true,
      },
    ]);

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    publicApi
      .getChatSuggestions()
      .then((response) => {
        if (response.length > 0) {
          setSuggestions(response);
        }
      })
      .catch(() => {
        setSuggestions(
          fallbackSuggestions,
        );
      });
  }, []);

  useEffect(() => {
    if (!open) {
      return;
    }

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading, open]);

  async function sendQuestion(
    requestedQuestion?: string,
  ) {
    const cleanQuestion = (
      requestedQuestion ?? question
    ).trim();

    if (!cleanQuestion || loading) {
      return;
    }

    const previousMessages = messages
      .filter(
        (message) =>
          message.id !== "welcome",
      )
      .slice(-6);

    const history: ChatHistoryMessage[] =
      previousMessages.map(
        (message) => ({
          role: message.role,
          content: message.content,
        }),
      );

    const userMessage: ChatMessage = {
      id: createMessageId(),
      role: "user",
      content: cleanQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response =
        await publicApi.askPortfolioChatbot({
          visitor_key: getVisitorKey(),
          question: cleanQuestion,
          history,
          top_k: 6,
        });

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: createMessageId(),
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          grounded: response.grounded,
          answerMode: response.answer_mode,
        },
      ]);
    } catch (error) {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: createMessageId(),
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "The portfolio assistant is currently unavailable.",
          grounded: false,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();
    void sendQuestion();
  }

  return (
    <>
      <button
        type="button"
        className="chat-launcher"
        aria-label="Open AI portfolio assistant"
        aria-expanded={open}
        aria-controls="portfolio-chat-widget"
        onClick={() => {
          setOpen(true);
        }}
      >
        <MessageCircle size={25} />

        <span>Ask AI</span>
      </button>

      {open && (
        <section
          id="portfolio-chat-widget"
          className="chat-widget"
          aria-label="AI portfolio assistant"
        >
          <header className="chat-header">
            <div>
              <span className="chat-avatar">
                <Bot size={22} />
              </span>

              <div>
                <strong>
                  Bajirao AI Assistant
                </strong>

                <span>
                  Portfolio + general AI
                </span>
              </div>
            </div>

            <button
              type="button"
              aria-label="Close chatbot"
              onClick={() => {
                setOpen(false);
              }}
            >
              <X size={21} />
            </button>
          </header>

          <div
            className="chat-messages"
            role="log"
            aria-live="polite"
            aria-relevant="additions text"
            aria-busy={loading}
          >
            {messages.map((message) => (
              <div
                className={`chat-message chat-message-${message.role}`}
                key={message.id}
              >
                <div className="chat-message-content">
                  {message.role ===
                    "assistant" && (
                    <span className="chat-mini-avatar">
                      <Sparkles
                        size={15}
                      />
                    </span>
                  )}

                  <p>{message.content}</p>
                  {message.role === "assistant" &&
                    message.answerMode && (
                      <span
                        className={`chat-answer-badge chat-answer-badge-${message.answerMode}`}
                      >
                        {message.answerMode === "portfolio"
                          ? "Portfolio answer"
                          : message.answerMode === "mixed"
                            ? "Portfolio + general answer"
                            : "General AI answer"}
                      </span>
                    )}
                </div>

                {message.sources &&
                  message.sources.length >
                    0 && (
                    <div className="chat-sources">
                      <strong>Sources</strong>

                      {message.sources
                        .slice(0, 4)
                        .map((source) => {
                          const sourceUrl =
                            resolveSourceUrl(
                              source.url,
                            );

                          if (!sourceUrl) {
                            return (
                              <span
                                key={`${source.source_type}-${source.source_id}-${source.title}`}
                              >
                                {source.title}
                              </span>
                            );
                          }

                          return (
                            <a
                              key={`${source.source_type}-${source.source_id}-${source.title}`}
                              href={sourceUrl}
                              target={
                                sourceUrl.startsWith(
                                  "http",
                                )
                                  ? "_blank"
                                  : undefined
                              }
                              rel={
                                sourceUrl.startsWith(
                                  "http",
                                )
                                  ? "noreferrer"
                                  : undefined
                              }
                            >
                              {source.title}
                              <ExternalLink
                                size={12}
                              />
                            </a>
                          );
                        })}
                    </div>
                  )}
              </div>
            ))}


            {loading && (
              <div className="chat-message chat-message-assistant">
                <div className="chat-message-content">
                  <span
                    className="chat-mini-avatar"
                    aria-hidden="true"
                  >
                    <Sparkles size={15} />
                  </span>

                  <p
                    className="chat-thinking"
                    aria-hidden="true"
                  >
                    <LoaderCircle
                      className="spin"
                      size={16}
                    />
                    Thinking and preparing answer...
                  </p>

                  <span className="sr-only">
                    The assistant is preparing a response.
                  </span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {messages.length <= 2 && (
            <div className="chat-suggestions">
              {suggestions
                .slice(0, 4)
                .map((suggestion) => (
                  <button
                    type="button"
                    key={suggestion}
                    onClick={() => {
                      void sendQuestion(
                        suggestion,
                      );
                    }}
                  >
                    {suggestion}
                  </button>
                ))}
            </div>
          )}

          <form
            className="chat-input-form"
            onSubmit={handleSubmit}
          >
            <input
              value={question}
              maxLength={1500}
              onChange={(event) => {
                setQuestion(
                  event.target.value,
                );
              }}
              placeholder="Ask about portfolio, coding, AI/ML, interviews or any general question..."
              aria-label="Ask portfolio assistant"
            />

            <button
              type="submit"
              aria-label="Send question"
              disabled={
                loading ||
                !question.trim()
              }
            >
              <Send size={18} />
            </button>
          </form>

          <p className="chat-disclaimer">
            Answers may use portfolio context or general AI depending on your question.
          </p>
        </section>
      )}
    </>
  );
}