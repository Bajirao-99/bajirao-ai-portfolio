import {
  BarChart3,
  Bot,
  BriefcaseBusiness,
  Download,
  Eye,
  FileSearch,
  LoaderCircle,
  Mail,
  RefreshCw,
  Users,
} from "lucide-react";

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

import { adminApi } from "../../lib/adminApi";
import { ApiError } from "../../lib/api";

import type {
  AnalyticsDashboard,
} from "../../types/admin";

function formatNumber(
  value: number,
): string {
  return new Intl.NumberFormat(
    "en-IN",
  ).format(value);
}

function formatDate(
  value: string,
): string {
  return new Intl.DateTimeFormat(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
    },
  ).format(new Date(value));
}

export default function AdminDashboardPage() {
  const {
    token,
    logout,
  } = useAdminAuth();

  const [days, setDays] =
    useState(30);

  const [analytics, setAnalytics] =
    useState<AnalyticsDashboard | null>(
      null,
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const loadAnalytics = useCallback(
    async () => {
      if (!token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await adminApi.getAnalytics(
            token,
            days,
          );

        setAnalytics(response);
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
            : "Could not load analytics.",
        );
      } finally {
        setLoading(false);
      }
    },
    [days, logout, token],
  );

  useEffect(() => {
    void loadAnalytics();
  }, [loadAnalytics]);

  const maximumDailyViews =
    useMemo(() => {
      if (
        !analytics ||
        analytics.daily_page_views.length ===
          0
      ) {
        return 1;
      }

      return Math.max(
        ...analytics.daily_page_views.map(
          (item) => item.views,
        ),
        1,
      );
    }, [analytics]);

  if (loading && !analytics) {
    return (
      <div className="admin-page-state">
        <LoaderCircle
          className="spin"
          size={38}
        />

        <p>
          Loading dashboard analytics
        </p>
      </div>
    );
  }

  return (
    <section>
      <div className="admin-page-heading">
        <div>
          <span className="eyebrow">
            Dashboard
          </span>

          <h1>
            Portfolio Overview
          </h1>

          <p>
            Monitor visitors, projects,
            downloads, messages and AI
            usage.
          </p>
        </div>

        <div className="admin-heading-actions">
          <select
            value={days}
            onChange={(event) => {
              setDays(
                Number(
                  event.target.value,
                ),
              );
            }}
          >
            <option value={7}>
              Last 7 days
            </option>

            <option value={30}>
              Last 30 days
            </option>

            <option value={90}>
              Last 90 days
            </option>

            <option value={365}>
              Last year
            </option>
          </select>

          <button
            type="button"
            className="admin-icon-button"
            aria-label="Refresh analytics"
            onClick={() => {
              void loadAnalytics();
            }}
          >
            <RefreshCw size={19} />
          </button>
        </div>
      </div>

      {error && (
        <div className="admin-alert admin-alert-error">
          {error}
        </div>
      )}

      {analytics && (
        <>
          <div className="admin-stat-grid">
            <article>
              <span className="admin-stat-icon">
                <Users size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_unique_visitors,
                  )}
                </strong>

                <span>
                  Unique Visitors
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <Eye size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_page_views,
                  )}
                </strong>

                <span>
                  Total Page Views
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <BriefcaseBusiness
                  size={22}
                />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_project_views,
                  )}
                </strong>

                <span>
                  Project Views
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <Download size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_resume_downloads,
                  )}
                </strong>

                <span>
                  Resume Downloads
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <Mail size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .new_contact_messages,
                  )}
                </strong>

                <span>
                  New Messages
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <FileSearch size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_job_match_analyses,
                  )}
                </strong>

                <span>
                  JD Analyses
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <Bot size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .total_chat_interactions,
                  )}
                </strong>

                <span>
                  Chat Interactions
                </span>
              </div>
            </article>

            <article>
              <span className="admin-stat-icon">
                <BarChart3 size={22} />
              </span>

              <div>
                <strong>
                  {formatNumber(
                    analytics.summary
                      .pending_interview_requests,
                  )}
                </strong>

                <span>
                  Pending Interviews
                </span>
              </div>
            </article>
          </div>

          <div className="admin-dashboard-grid">
            <article className="admin-panel admin-chart-panel">
              <div className="admin-panel-heading">
                <div>
                  <h2>
                    Daily Page Views
                  </h2>

                  <p>
                    Activity during the
                    selected period.
                  </p>
                </div>

                <BarChart3 size={22} />
              </div>

              {analytics.daily_page_views
                .length === 0 ? (
                <div className="admin-empty-state">
                  No page views recorded
                  during this period.
                </div>
              ) : (
                <div className="admin-bar-chart">
                  {analytics.daily_page_views.map(
                    (item) => (
                      <div
                        className="admin-chart-column"
                        key={item.view_date}
                      >
                        <span
                          className="admin-chart-bar"
                          style={{
                            height: `${Math.max(
                              8,
                              (item.views /
                                maximumDailyViews) *
                                100,
                            )}%`,
                          }}
                          title={`${item.views} views`}
                        />

                        <strong>
                          {item.views}
                        </strong>

                        <small>
                          {formatDate(
                            item.view_date,
                          )}
                        </small>
                      </div>
                    ),
                  )}
                </div>
              )}
            </article>

            <article className="admin-panel">
              <div className="admin-panel-heading">
                <div>
                  <h2>Top Pages</h2>

                  <p>
                    Most visited portfolio
                    pages.
                  </p>
                </div>

                <Eye size={22} />
              </div>

              <div className="admin-ranking-list">
                {analytics.top_pages.map(
                  (page, index) => (
                    <div
                      key={page.page_path}
                    >
                      <span>
                        {index + 1}
                      </span>

                      <strong>
                        {page.page_path}
                      </strong>

                      <small>
                        {page.views} views
                      </small>
                    </div>
                  ),
                )}
              </div>
            </article>

            <article className="admin-panel">
              <div className="admin-panel-heading">
                <div>
                  <h2>Top Projects</h2>

                  <p>
                    Projects ranked by
                    public views.
                  </p>
                </div>

                <BriefcaseBusiness
                  size={22}
                />
              </div>

              <div className="admin-ranking-list">
                {analytics.top_projects.map(
                  (project, index) => (
                    <div key={project.id}>
                      <span>
                        {index + 1}
                      </span>

                      <strong>
                        {project.title}
                      </strong>

                      <small>
                        {
                          project.view_count
                        }{" "}
                        views
                      </small>
                    </div>
                  ),
                )}
              </div>
            </article>

            <article className="admin-panel">
              <div className="admin-panel-heading">
                <div>
                  <h2>
                    Resume Downloads
                  </h2>

                  <p>
                    Downloads by resume
                    version.
                  </p>
                </div>

                <Download size={22} />
              </div>

              <div className="admin-ranking-list">
                {analytics.resume_downloads.map(
                  (resume, index) => (
                    <div key={resume.id}>
                      <span>
                        {index + 1}
                      </span>

                      <strong>
                        {resume.title}
                      </strong>

                      <small>
                        {
                          resume.download_count
                        }{" "}
                        downloads
                      </small>
                    </div>
                  ),
                )}
              </div>
            </article>
          </div>
        </>
      )}
    </section>
  );
}