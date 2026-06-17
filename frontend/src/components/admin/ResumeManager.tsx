import {
  FileText,
  LoaderCircle,
  Save,
  Trash2,
  Upload,
} from "lucide-react";

import {
  type FormEvent,
  useState,
} from "react";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

import {
  contentAdminApi,
} from "../../lib/contentAdminApi";

import type {
  Resume,
} from "../../types/portfolio";

interface ResumeManagerProps {
  resumes: Resume[];
  onChanged: () => Promise<void>;
}

function formatFileSize(
  bytes: number,
): string {
  if (bytes < 1024 * 1024) {
    return `${Math.max(
      1,
      Math.round(bytes / 1024),
    )} KB`;
  }

  return `${(
    bytes /
    (1024 * 1024)
  ).toFixed(1)} MB`;
}

export default function ResumeManager({
  resumes,
  onChanged,
}: ResumeManagerProps) {
  const { token } = useAdminAuth();

  const [title, setTitle] =
    useState("");

  const [resumeType, setResumeType] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [
    displayOrder,
    setDisplayOrder,
  ] = useState(0);

  const [isVisible, setIsVisible] =
    useState(true);

  const [file, setFile] =
    useState<File | null>(null);

  const [uploading, setUploading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleUpload(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!token || !file) {
      setError(
        "Select a PDF resume.",
      );
      return;
    }

    setUploading(true);
    setError(null);

    try {
      await contentAdminApi.uploadResume(
        token,
        {
          title: title.trim(),
          resumeType:
            resumeType.trim().toLowerCase(),
          description:
            description.trim(),
          displayOrder,
          isVisible,
          file,
        },
      );

      setTitle("");
      setResumeType("");
      setDescription("");
      setDisplayOrder(0);
      setIsVisible(true);
      setFile(null);

      await onChanged();
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "Could not upload resume.",
      );
    } finally {
      setUploading(false);
    }
  }

  async function handleVisibilityChange(
    resume: Resume,
  ) {
    if (!token) {
      return;
    }

    try {
      await contentAdminApi.updateResume(
        token,
        resume.id,
        {
          is_visible:
            !resume.is_visible,
        },
      );

      await onChanged();
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Could not update resume.",
      );
    }
  }

  async function handleReplace(
    resume: Resume,
    replacementFile: File | null,
  ) {
    if (!token || !replacementFile) {
      return;
    }

    setError(null);

    try {
      await contentAdminApi.replaceResumeFile(
        token,
        resume.id,
        replacementFile,
      );

      await onChanged();
    } catch (replaceError) {
      setError(
        replaceError instanceof Error
          ? replaceError.message
          : "Could not replace resume.",
      );
    }
  }

  async function handleDelete(
    resumeId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this resume and its PDF file?",
      )
    ) {
      return;
    }

    try {
      await contentAdminApi.deleteResume(
        token,
        resumeId,
      );

      await onChanged();
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete resume.",
      );
    }
  }

  return (
    <section>
      <div className="content-section-heading">
        <div>
          <span className="eyebrow">
            Resume Management
          </span>

          <h2>Resume Versions</h2>

          <p>
            Upload and manage Software
            Engineer, AI/ML and Academic
            resume PDFs.
          </p>
        </div>

        <FileText size={30} />
      </div>

      <form
        className="resume-upload-form"
        onSubmit={handleUpload}
      >
        <div className="content-editor-grid">
          <label className="content-field">
            Resume Title
            <input
              required
              minLength={2}
              maxLength={200}
              value={title}
              onChange={(event) => {
                setTitle(
                  event.target.value,
                );
              }}
              placeholder="Software Engineer Resume"
            />
          </label>

          <label className="content-field">
            Resume Type
            <input
              required
              pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$"
              value={resumeType}
              onChange={(event) => {
                setResumeType(
                  event.target.value,
                );
              }}
              placeholder="software-engineer"
            />
          </label>

          <label className="content-field content-field-full">
            Description
            <textarea
              rows={4}
              value={description}
              onChange={(event) => {
                setDescription(
                  event.target.value,
                );
              }}
            />
          </label>

          <label className="content-field">
            Display Order
            <input
              type="number"
              min={0}
              value={displayOrder}
              onChange={(event) => {
                setDisplayOrder(
                  Number(
                    event.target.value,
                  ),
                );
              }}
            />
          </label>

          <label className="content-field">
            PDF File
            <input
              required
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                setFile(
                  event.target.files?.[0] ??
                    null,
                );
              }}
            />
          </label>

          <label className="content-checkbox-field">
            <input
              type="checkbox"
              checked={isVisible}
              onChange={(event) => {
                setIsVisible(
                  event.target.checked,
                );
              }}
            />

            <span>Visible</span>
          </label>
        </div>

        {error && (
          <div className="admin-alert admin-alert-error">
            {error}
          </div>
        )}

        <button
          type="submit"
          className="button button-primary"
          disabled={uploading}
        >
          {uploading ? (
            <LoaderCircle
              className="spin"
              size={18}
            />
          ) : (
            <Upload size={18} />
          )}

          Upload Resume
        </button>
      </form>

      <div className="resume-admin-list">
        {resumes.map((resume) => (
          <article key={resume.id}>
            <span className="resume-admin-icon">
              <FileText size={24} />
            </span>

            <div className="resume-admin-details">
              <strong>
                {resume.title}
              </strong>

              <span>
                {resume.resume_type}
              </span>

              <small>
                {formatFileSize(
                  resume.file_size_bytes,
                )}
                {" • "}
                {resume.download_count} downloads
              </small>
            </div>

            <div className="resume-admin-actions">
              <label>
                <Upload size={16} />
                Replace PDF

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(event) => {
                    void handleReplace(
                      resume,
                      event.target
                        .files?.[0] ??
                        null,
                    );

                    event.target.value =
                      "";
                  }}
                />
              </label>

              <button
                type="button"
                onClick={() => {
                  void handleVisibilityChange(
                    resume,
                  );
                }}
              >
                <Save size={16} />

                {resume.is_visible
                  ? "Hide"
                  : "Show"}
              </button>

              <button
                type="button"
                className="resume-delete-button"
                onClick={() => {
                  void handleDelete(
                    resume.id,
                  );
                }}
              >
                <Trash2 size={16} />
                Delete
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}