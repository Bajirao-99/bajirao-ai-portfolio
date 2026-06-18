import {
  ImagePlus,
  LoaderCircle,
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
  resolveApiUrl,
} from "../../lib/api";

import {
  contentAdminApi,
} from "../../lib/contentAdminApi";

import type {
  Project,
} from "../../types/portfolio";

interface ProjectImageManagerProps {
  project: Project;
  onChanged: () => Promise<void>;
}

export default function ProjectImageManager({
  project,
  onChanged,
}: ProjectImageManagerProps) {
  const { token } = useAdminAuth();

  const [file, setFile] =
    useState<File | null>(null);

  const [altText, setAltText] =
    useState("");

  const [caption, setCaption] =
    useState("");

  const [
    displayOrder,
    setDisplayOrder,
  ] = useState(0);

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
        "Select an image file.",
      );
      return;
    }

    setUploading(true);
    setError(null);

    try {
      await contentAdminApi.uploadProjectImage(
        token,
        project.id,
        {
          file,
          altText: altText.trim(),
          caption: caption.trim(),
          displayOrder,
        },
      );

      setFile(null);
      setAltText("");
      setCaption("");
      setDisplayOrder(0);

      await onChanged();
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "Could not upload image.",
      );
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(
    imageId: number,
  ) {
    if (
      !token ||
      !window.confirm(
        "Delete this project image?",
      )
    ) {
      return;
    }

    setError(null);

    try {
      await contentAdminApi.deleteProjectImage(
        token,
        imageId,
      );

      await onChanged();
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete image.",
      );
    }
  }

  return (
    <section className="project-image-manager">
      <div className="content-section-heading">
        <div>
          <span className="eyebrow">
            Project Media
          </span>

          <h2>{project.title}</h2>

          <p>
            Upload validated JPG, PNG or
            WebP screenshots.
          </p>
        </div>

        <ImagePlus size={28} />
      </div>

      <form
        className="project-image-upload-form"
        onSubmit={handleUpload}
      >
        <label>
          Image File
          <input
            required
            type="file"
            accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
            onChange={(event) => {
              setFile(
                event.target.files?.[0] ??
                  null,
              );
            }}
          />
        </label>

        <label>
          Alternative Text
          <input
            required
            minLength={2}
            maxLength={250}
            value={altText}
            onChange={(event) => {
              setAltText(
                event.target.value,
              );
            }}
            placeholder="RecruitAI candidate ranking dashboard"
          />
        </label>

        <label>
          Caption
          <input
            maxLength={500}
            value={caption}
            onChange={(event) => {
              setCaption(
                event.target.value,
              );
            }}
            placeholder="Optional caption"
          />
        </label>

        <label>
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

          Upload Screenshot
        </button>
      </form>

      {error && (
        <div className="admin-alert admin-alert-error">
          {error}
        </div>
      )}

      {project.images.length === 0 ? (
        <div className="admin-empty-panel project-image-empty">
          <ImagePlus size={32} />

          <h3>No screenshots uploaded</h3>
        </div>
      ) : (
        <div className="project-admin-image-grid">
          {project.images.map(
            (image) => {
              const imageUrl =
                resolveApiUrl(
                  image.image_url,
                );

              return (
                <article key={image.id}>
                  {imageUrl && (
                    <img
                      src={imageUrl}
                      alt={
                        image.alt_text ||
                        "Project image preview"
                      }
                      loading="lazy"
                      decoding="async"
                      width={1200}
                      height={675}
                    />
                  )}

                  <div>
                    <strong>
                      {image.alt_text}
                    </strong>

                    {image.caption && (
                      <p>
                        {image.caption}
                      </p>
                    )}

                    <button
                      type="button"
                      onClick={() => {
                        void handleDelete(
                          image.id,
                        );
                      }}
                    >
                      <Trash2
                        size={16}
                      />
                      Delete
                    </button>
                  </div>
                </article>
              );
            },
          )}
        </div>
      )}
    </section>
  );
}