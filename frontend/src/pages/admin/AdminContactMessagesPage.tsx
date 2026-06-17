import {
  LoaderCircle,
  Mail,
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
  ContactMessageAdmin,
} from "../../types/admin";

const contactStatuses = [
  "new",
  "read",
  "replied",
  "archived",
];

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

export default function AdminContactMessagesPage() {
  const {
    token,
    logout,
  } = useAdminAuth();

  const [statusFilter, setStatusFilter] =
    useState("");

  const [messages, setMessages] =
    useState<ContactMessageAdmin[]>([]);

  const [selectedMessage, setSelectedMessage] =
    useState<ContactMessageAdmin | null>(
      null,
    );

  const [editStatus, setEditStatus] =
    useState("new");

  const [adminNotes, setAdminNotes] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const loadMessages = useCallback(
    async () => {
      if (!token) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await adminApi.getContactMessages(
            token,
            statusFilter || undefined,
          );

        setMessages(response);
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
            : "Could not load messages.",
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
    void loadMessages();
  }, [loadMessages]);

  function selectMessage(
    message: ContactMessageAdmin,
  ) {
    setSelectedMessage(message);
    setEditStatus(message.status);
    setAdminNotes(
      message.admin_notes ?? "",
    );
  }

  async function handleUpdate(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!token || !selectedMessage) {
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const updatedMessage =
        await adminApi.updateContactMessage(
          token,
          selectedMessage.id,
          {
            status: editStatus,
            admin_notes:
              adminNotes.trim() || null,
          },
        );

      setMessages((currentMessages) =>
        currentMessages.map(
          (message) =>
            message.id ===
            updatedMessage.id
              ? updatedMessage
              : message,
        ),
      );

      setSelectedMessage(
        updatedMessage,
      );
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Could not update message.",
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(
    messageId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this contact message?",
      )
    ) {
      return;
    }

    try {
      await adminApi.deleteContactMessage(
        token,
        messageId,
      );

      setMessages((currentMessages) =>
        currentMessages.filter(
          (message) =>
            message.id !== messageId,
        ),
      );

      if (
        selectedMessage?.id === messageId
      ) {
        setSelectedMessage(null);
      }
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete message.",
      );
    }
  }

  return (
    <section>
      <div className="admin-page-heading">
        <div>
          <span className="eyebrow">
            Communication
          </span>

          <h1>
            Contact Messages
          </h1>

          <p>
            Review and manage messages
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

            {contactStatuses.map(
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
              void loadMessages();
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

          <p>Loading messages</p>
        </div>
      ) : messages.length === 0 ? (
        <div className="admin-empty-panel">
          <Mail size={34} />
          <h2>No messages found</h2>
          <p>
            Submitted contact messages will
            appear here.
          </p>
        </div>
      ) : (
        <div className="admin-table-panel">
          <div className="admin-table-scroll">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Sender</th>
                  <th>Subject</th>
                  <th>Status</th>
                  <th>Received</th>
                  <th />
                </tr>
              </thead>

              <tbody>
                {messages.map((message) => (
                  <tr key={message.id}>
                    <td>
                      <strong>
                        {message.name}
                      </strong>

                      <span>
                        {message.email}
                      </span>
                    </td>

                    <td>
                      {message.subject}
                    </td>

                    <td>
                      <span
                        className={`admin-status admin-status-${message.status}`}
                      >
                        {message.status}
                      </span>
                    </td>

                    <td>
                      {formatDateTime(
                        message.created_at,
                      )}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="admin-table-action"
                        onClick={() => {
                          selectMessage(
                            message,
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

      {selectedMessage && (
        <div className="admin-detail-overlay">
          <button
            type="button"
            className="admin-detail-backdrop"
            aria-label="Close message"
            onClick={() => {
              setSelectedMessage(null);
            }}
          />

          <aside className="admin-detail-panel">
            <header>
              <div>
                <span>
                  Contact Message
                </span>

                <h2>
                  {selectedMessage.subject}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedMessage(null);
                }}
              >
                <X size={21} />
              </button>
            </header>

            <div className="admin-detail-body">
              <div className="admin-detail-field">
                <span>Sender</span>
                <strong>
                  {selectedMessage.name}
                </strong>
              </div>

              <div className="admin-detail-field">
                <span>Email</span>

                <a
                  href={`mailto:${selectedMessage.email}`}
                >
                  {selectedMessage.email}
                </a>
              </div>

              {selectedMessage.phone && (
                <div className="admin-detail-field">
                  <span>Phone</span>

                  <a
                    href={`tel:${selectedMessage.phone}`}
                  >
                    {selectedMessage.phone}
                  </a>
                </div>
              )}

              <div className="admin-detail-field">
                <span>Received</span>

                <strong>
                  {formatDateTime(
                    selectedMessage.created_at,
                  )}
                </strong>
              </div>

              <div className="admin-detail-message">
                <span>Message</span>

                <p>
                  {selectedMessage.message}
                </p>
              </div>

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
                    {contactStatuses.map(
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
                    selectedMessage.id,
                  );
                }}
              >
                <Trash2 size={17} />
                Delete Message
              </button>
            </div>
          </aside>
        </div>
      )}
    </section>
  );
}