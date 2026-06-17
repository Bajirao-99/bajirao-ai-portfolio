import {
  Bot,
  FileSearch,
  LoaderCircle,
  RefreshCw,
  Trash2,
} from "lucide-react";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

import { adminApi } from "../../lib/adminApi";
import { ApiError } from "../../lib/api";

import type {
  ChatInteractionHistory,
  JobMatchHistory,
} from "../../types/admin";

type ActivityTab =
  | "job-matches"
  | "chat";

function formatDateTime(
  value: string,
): string {
  return new Intl.DateTimeFormat(
    "en-IN",
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(new Date(value));
}

export default function AdminAIActivityPage() {
  const {
    token,
    logout,
  } = useAdminAuth();

  const [activeTab, setActiveTab] =
    useState<ActivityTab>(
      "job-matches",
    );

  const [jobMatches, setJobMatches] =
    useState<JobMatchHistory[]>([]);

  const [chatInteractions, setChatInteractions] =
    useState<
      ChatInteractionHistory[]
    >([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const loadActivity = useCallback(
    async () => {
      if (!token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const [
          jobMatchResponse,
          chatResponse,
        ] = await Promise.all([
          adminApi.getJobMatchHistory(
            token,
          ),
          adminApi.getChatInteractions(
            token,
          ),
        ]);

        setJobMatches(
          jobMatchResponse,
        );

        setChatInteractions(
          chatResponse,
        );
      } catch (loadError) {
        if (
          loadError instanceof ApiError &&
          loadError.status === 401
        ) {
          logout();
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Could not load AI activity.",
        );
      } finally {
        setLoading(false);
      }
    },
    [logout, token],
  );

  useEffect(() => {
    void loadActivity();
  }, [loadActivity]);

  async function removeJobMatch(
    analysisId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this job match analysis?",
      )
    ) {
      return;
    }

    try {
      await adminApi.deleteJobMatchAnalysis(
        token,
        analysisId,
      );

      setJobMatches(
        (currentItems) =>
          currentItems.filter(
            (item) =>
              item.id !== analysisId,
          ),
      );
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete analysis.",
      );
    }
  }

  async function removeChatInteraction(
    interactionId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this chat interaction?",
      )
    ) {
      return;
    }

    try {
      await adminApi.deleteChatInteraction(
        token,
        interactionId,
      );

      setChatInteractions(
        (currentItems) =>
          currentItems.filter(
            (item) =>
              item.id !== interactionId,
          ),
      );
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete interaction.",
      );
    }
  }

  return (
    <section>
      <div className="admin-page-heading">
        <div>
          <span className="eyebrow">
            Artificial Intelligence
          </span>

          <h1>AI Activity</h1>

          <p>
            Review job-description analyses
            and portfolio-chat interactions.
          </p>
        </div>

        <button
          type="button"
          className="admin-icon-button"
          onClick={() => {
            void loadActivity();
          }}
        >
          <RefreshCw size={19} />
        </button>
      </div>

      <div className="admin-tabs">
        <button
          type="button"
          className={
            activeTab === "job-matches"
              ? "admin-tab-active"
              : ""
          }
          onClick={() => {
            setActiveTab(
              "job-matches",
            );
          }}
        >
          <FileSearch size={18} />
          JD Analyses
          <span>{jobMatches.length}</span>
        </button>

        <button
          type="button"
          className={
            activeTab === "chat"
              ? "admin-tab-active"
              : ""
          }
          onClick={() => {
            setActiveTab("chat");
          }}
        >
          <Bot size={18} />
          Chat Interactions
          <span>
            {chatInteractions.length}
          </span>
        </button>
      </div>

      {error && (
        <div className="admin-alert admin-alert-error">
          {error}
        </div>
      )}

      {loading ? (
        <div className="admin-page-state">
          <LoaderCircle
            className="spin"
            size={36}
          />

          <p>Loading AI activity</p>
        </div>
      ) : activeTab ===
        "job-matches" ? (
        <div className="admin-activity-list">
          {jobMatches.length === 0 ? (
            <div className="admin-empty-panel">
              <FileSearch size={34} />

              <h2>
                No JD analyses found
              </h2>
            </div>
          ) : (
            jobMatches.map((analysis) => (
              <article
                className="admin-activity-card"
                key={analysis.id}
              >
                <div className="admin-activity-score">
                  <strong>
                    {Math.round(
                      analysis.overall_match_score,
                    )}
                    %
                  </strong>

                  <span>
                    {analysis.match_level}
                  </span>
                </div>

                <div className="admin-activity-content">
                  <span className="admin-activity-date">
                    {formatDateTime(
                      analysis.created_at,
                    )}
                  </span>

                  <h2>
                    {analysis.job_title ??
                      "Untitled Role"}
                  </h2>

                  <p>
                    {analysis.company_name ??
                      "Company not provided"}
                  </p>

                  <div className="admin-chip-group">
                    {analysis.matched_skills
                      .slice(0, 8)
                      .map((skill) => (
                        <span
                          className="admin-chip admin-chip-success"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))}
                  </div>

                  {analysis.missing_skills
                    .length > 0 && (
                    <div className="admin-chip-group">
                      {analysis.missing_skills
                        .slice(0, 6)
                        .map((skill) => (
                          <span
                            className="admin-chip admin-chip-warning"
                            key={skill}
                          >
                            {skill}
                          </span>
                        ))}
                    </div>
                  )}

                  <small>
                    Recommended resume:{" "}
                    {analysis.recommended_resume_type.replace(
                      /-/g,
                      " ",
                    )}
                  </small>
                </div>

                <button
                  type="button"
                  className="admin-delete-icon"
                  aria-label="Delete analysis"
                  onClick={() => {
                    void removeJobMatch(
                      analysis.id,
                    );
                  }}
                >
                  <Trash2 size={18} />
                </button>
              </article>
            ))
          )}
        </div>
      ) : (
        <div className="admin-activity-list">
          {chatInteractions.length ===
          0 ? (
            <div className="admin-empty-panel">
              <Bot size={34} />

              <h2>
                No chat interactions found
              </h2>
            </div>
          ) : (
            chatInteractions.map(
              (interaction) => (
                <article
                  className="admin-chat-record"
                  key={interaction.id}
                >
                  <div className="admin-chat-record-header">
                    <div>
                      <span>
                        {formatDateTime(
                          interaction.created_at,
                        )}
                      </span>

                      <strong>
                        {interaction.grounded
                          ? "Grounded Answer"
                          : "Unsupported Question"}
                      </strong>
                    </div>

                    <button
                      type="button"
                      className="admin-delete-icon"
                      onClick={() => {
                        void removeChatInteraction(
                          interaction.id,
                        );
                      }}
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>

                  <div className="admin-chat-question">
                    <span>Question</span>

                    <p>
                      {interaction.question}
                    </p>
                  </div>

                  <div className="admin-chat-answer">
                    <span>Answer</span>

                    <p>
                      {interaction.answer}
                    </p>
                  </div>

                  <div className="admin-chat-metadata">
                    <span>
                      Confidence:{" "}
                      {Math.round(
                        interaction.confidence_score,
                      )}
                      %
                    </span>

                    <span>
                      Sources:{" "}
                      {
                        interaction
                          .source_refs.length
                      }
                    </span>

                    <span>
                      {
                        interaction.model_name
                      }
                    </span>
                  </div>
                </article>
              ),
            )
          )}
        </div>
      )}
    </section>
  );
}