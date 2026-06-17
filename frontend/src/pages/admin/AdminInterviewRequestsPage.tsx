import {
  CalendarDays,
  LoaderCircle,
  RefreshCw,
  Save,
  Trash2,
  X,
} from "lucide-react";

import {
  type FormEvent,
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
  InterviewRequestAdmin,
} from "../../types/admin";

const interviewStatuses = [
  "pending",
  "reviewed",
  "scheduled",
  "completed",
  "declined",
  "archived",
];

function formatDateTime(
  value: string | null,
): string {
  if (!value) {
    return "Not specified";
  }

  return new Intl.DateTimeFormat(
    "en-IN",
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(new Date(value));
}

export default function AdminInterviewRequestsPage() {
  const {
    token,
    logout,
  } = useAdminAuth();

  const [statusFilter, setStatusFilter] =
    useState("");

  const [requests, setRequests] =
    useState<InterviewRequestAdmin[]>(
      [],
    );

  const [selectedRequest, setSelectedRequest] =
    useState<InterviewRequestAdmin | null>(
      null,
    );

  const [editStatus, setEditStatus] =
    useState("pending");

  const [adminNotes, setAdminNotes] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const loadRequests = useCallback(
    async () => {
      if (!token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await adminApi.getInterviewRequests(
            token,
            statusFilter || undefined,
          );

        setRequests(response);
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
            : "Could not load interview requests.",
        );
      } finally {
        setLoading(false);
      }
    },
    [
      logout,
      statusFilter,
      token,
    ],
  );

  useEffect(() => {
    void loadRequests();
  }, [loadRequests]);

  function selectRequest(
    request: InterviewRequestAdmin,
  ) {
    setSelectedRequest(request);
    setEditStatus(request.status);
    setAdminNotes(
      request.admin_notes ?? "",
    );
  }

  async function handleUpdate(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!token || !selectedRequest) {
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const updatedRequest =
        await adminApi.updateInterviewRequest(
          token,
          selectedRequest.id,
          {
            status: editStatus,
            admin_notes:
              adminNotes.trim() || null,
          },
        );

      setRequests((currentRequests) =>
        currentRequests.map(
          (request) =>
            request.id ===
            updatedRequest.id
              ? updatedRequest
              : request,
        ),
      );

      setSelectedRequest(
        updatedRequest,
      );
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Could not update request.",
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(
    requestId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this interview request?",
      )
    ) {
      return;
    }

    try {
      await adminApi.deleteInterviewRequest(
        token,
        requestId,
      );

      setRequests((currentRequests) =>
        currentRequests.filter(
          (request) =>
            request.id !== requestId,
        ),
      );

      if (
        selectedRequest?.id === requestId
      ) {
        setSelectedRequest(null);
      }
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete request.",
      );
    }
  }

  return (
    <section>
      <div className="admin-page-heading">
        <div>
          <span className="eyebrow">
            Recruitment
          </span>

          <h1>
            Interview Requests
          </h1>

          <p>
            Review interview invitations
            submitted through the public
            portfolio.
          </p>
        </div>

        <div className="admin-heading-actions">
          <select
            value={statusFilter}
            onChange={(event) => {
              setStatusFilter(
                event.target.value,
              );
            }}
          >
            <option value="">
              All statuses
            </option>

            {interviewStatuses.map(
              (status) => (
                <option
                  value={status}
                  key={status}
                >
                  {status}
                </option>
              ),
            )}
          </select>

          <button
            type="button"
            className="admin-icon-button"
            onClick={() => {
              void loadRequests();
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

      {loading ? (
        <div className="admin-page-state">
          <LoaderCircle
            className="spin"
            size={36}
          />

          <p>
            Loading interview requests
          </p>
        </div>
      ) : requests.length === 0 ? (
        <div className="admin-empty-panel">
          <CalendarDays size={34} />

          <h2>
            No interview requests found
          </h2>

          <p>
            New interview requests will
            appear here.
          </p>
        </div>
      ) : (
        <div className="admin-table-panel">
          <div className="admin-table-scroll">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Recruiter</th>
                  <th>Company and Role</th>
                  <th>Preferred Time</th>
                  <th>Status</th>
                  <th />
                </tr>
              </thead>

              <tbody>
                {requests.map((request) => (
                  <tr key={request.id}>
                    <td>
                      <strong>
                        {request.name}
                      </strong>

                      <span>
                        {request.email}
                      </span>
                    </td>

                    <td>
                      <strong>
                        {request.company}
                      </strong>

                      <span>
                        {request.role}
                      </span>
                    </td>

                    <td>
                      {formatDateTime(
                        request.preferred_datetime,
                      )}
                    </td>

                    <td>
                      <span
                        className={`admin-status admin-status-${request.status}`}
                      >
                        {request.status}
                      </span>
                    </td>

                    <td>
                      <button
                        type="button"
                        className="admin-table-action"
                        onClick={() => {
                          selectRequest(
                            request,
                          );
                        }}
                      >
                        Open
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {selectedRequest && (
        <div className="admin-detail-overlay">
          <button
            type="button"
            className="admin-detail-backdrop"
            aria-label="Close request"
            onClick={() => {
              setSelectedRequest(null);
            }}
          />

          <aside className="admin-detail-panel">
            <header>
              <div>
                <span>
                  Interview Request
                </span>

                <h2>
                  {selectedRequest.role}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedRequest(null);
                }}
              >
                <X size={21} />
              </button>
            </header>

            <div className="admin-detail-body">
              <div className="admin-detail-field">
                <span>Recruiter</span>
                <strong>
                  {selectedRequest.name}
                </strong>
              </div>

              <div className="admin-detail-field">
                <span>Company</span>
                <strong>
                  {
                    selectedRequest.company
                  }
                </strong>
              </div>

              <div className="admin-detail-field">
                <span>Email</span>

                <a
                  href={`mailto:${selectedRequest.email}`}
                >
                  {selectedRequest.email}
                </a>
              </div>

              {selectedRequest.phone && (
                <div className="admin-detail-field">
                  <span>Phone</span>

                  <a
                    href={`tel:${selectedRequest.phone}`}
                  >
                    {selectedRequest.phone}
                  </a>
                </div>
              )}

              <div className="admin-detail-field">
                <span>
                  Preferred Time
                </span>

                <strong>
                  {formatDateTime(
                    selectedRequest.preferred_datetime,
                  )}
                </strong>
              </div>

              <div className="admin-detail-field">
                <span>Timezone</span>

                <strong>
                  {selectedRequest.timezone ??
                    "Not specified"}
                </strong>
              </div>

              <div className="admin-detail-field">
                <span>Meeting Mode</span>

                <strong>
                  {selectedRequest.meeting_mode ??
                    "Not specified"}
                </strong>
              </div>

              {selectedRequest.message && (
                <div className="admin-detail-message">
                  <span>Message</span>

                  <p>
                    {selectedRequest.message}
                  </p>
                </div>
              )}

              <form
                className="admin-edit-form"
                onSubmit={handleUpdate}
              >
                <label>
                  Status
                  <select
                    value={editStatus}
                    onChange={(event) => {
                      setEditStatus(
                        event.target.value,
                      );
                    }}
                  >
                    {interviewStatuses.map(
                      (status) => (
                        <option
                          value={status}
                          key={status}
                        >
                          {status}
                        </option>
                      ),
                    )}
                  </select>
                </label>

                <label>
                  Admin Notes
                  <textarea
                    rows={5}
                    value={adminNotes}
                    onChange={(event) => {
                      setAdminNotes(
                        event.target.value,
                      );
                    }}
                    placeholder="Private notes..."
                  />
                </label>

                <button
                  type="submit"
                  className="button button-primary button-full"
                  disabled={saving}
                >
                  {saving ? (
                    <LoaderCircle
                      className="spin"
                      size={18}
                    />
                  ) : (
                    <Save size={18} />
                  )}

                  Save Changes
                </button>
              </form>

              <button
                type="button"
                className="admin-danger-button"
                onClick={() => {
                  void handleDelete(
                    selectedRequest.id,
                  );
                }}
              >
                <Trash2 size={17} />
                Delete Request
              </button>
            </div>
          </aside>
        </div>
      )}
    </section>
  );
}