import {
  LoaderCircle,
  Save,
  X,
} from "lucide-react";

import {
  type FormEvent,
  useMemo,
  useState,
} from "react";

import type {
  AdminContentRecord,
  AdminFieldConfig,
  AdminResourceConfig,
} from "../../types/contentAdmin";

interface ContentEditorModalProps {
  resource: AdminResourceConfig;
  record: AdminContentRecord | null;
  saving: boolean;
  error: string | null;
  onClose: () => void;
  onSave: (
    data: Record<string, unknown>,
  ) => Promise<void>;
}

function fieldInitialValue(
  field: AdminFieldConfig,
  record: AdminContentRecord | null,
): string | boolean {
  const value = record?.[field.name];

  if (field.type === "checkbox") {
    if (typeof value === "boolean") {
      return value;
    }

    return field.name === "is_visible";
  }

  if (field.type === "tags") {
    return Array.isArray(value)
      ? value.join(", ")
      : "";
  }

  if (field.type === "json") {
    if (
      value &&
      typeof value === "object"
    ) {
      return JSON.stringify(
        value,
        null,
        2,
      );
    }

    return "";
  }

  if (
    field.type === "date" &&
    typeof value === "string"
  ) {
    return value.slice(0, 10);
  }

  if (
    value === null ||
    value === undefined
  ) {
    if (field.type === "number") {
      return field.name ===
        "display_order"
        ? "0"
        : "";
    }

    return "";
  }

  return String(value);
}

function createInitialState(
  resource: AdminResourceConfig,
  record: AdminContentRecord | null,
): Record<string, string | boolean> {
  return Object.fromEntries(
    resource.fields.map((field) => [
      field.name,
      fieldInitialValue(
        field,
        record,
      ),
    ]),
  );
}

function createPayload(
  fields: AdminFieldConfig[],
  formValues: Record<
    string,
    string | boolean
  >,
): Record<string, unknown> {
  const payload: Record<
    string,
    unknown
  > = {};

  for (const field of fields) {
    const value =
      formValues[field.name];

    if (field.type === "checkbox") {
      payload[field.name] =
        Boolean(value);

      continue;
    }

    const textValue =
      typeof value === "string"
        ? value.trim()
        : "";

    if (field.type === "number") {
      payload[field.name] =
        textValue === ""
          ? null
          : Number(textValue);

      continue;
    }

    if (field.type === "tags") {
      payload[field.name] =
        textValue === ""
          ? []
          : textValue
              .split(",")
              .map((item) =>
                item.trim(),
              )
              .filter(Boolean);

      continue;
    }

    if (field.type === "json") {
      payload[field.name] =
        textValue === ""
          ? {}
          : JSON.parse(textValue);

      continue;
    }

    payload[field.name] =
      textValue === ""
        ? null
        : textValue;
  }

  return payload;
}

export default function ContentEditorModal({
  resource,
  record,
  saving,
  error,
  onClose,
  onSave,
}: ContentEditorModalProps) {
  const initialState = useMemo(
    () =>
      createInitialState(
        resource,
        record,
      ),
    [resource, record],
  );

  const [formValues, setFormValues] =
    useState(initialState);

  const [formError, setFormError] =
    useState<string | null>(null);

  function updateField(
    fieldName: string,
    value: string | boolean,
  ) {
    setFormValues(
      (currentValues) => ({
        ...currentValues,
        [fieldName]: value,
      }),
    );
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setFormError(null);

    try {
      const payload = createPayload(
        resource.fields,
        formValues,
      );

      await onSave(payload);
    } catch (submitError) {
      setFormError(
        submitError instanceof Error
          ? submitError.message
          : "Could not prepare the form data.",
      );
    }
  }

  return (
    <div className="content-modal-overlay">
      <button
        type="button"
        className="content-modal-backdrop"
        aria-label="Close editor"
        onClick={onClose}
      />

      <section className="content-modal">
        <header>
          <div>
            <span>
              {record
                ? "Edit Record"
                : "Create Record"}
            </span>

            <h2>
              {record
                ? `Edit ${resource.singularLabel}`
                : `Add ${resource.singularLabel}`}
            </h2>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close editor"
          >
            <X size={21} />
          </button>
        </header>

        <form
          className="content-editor-form"
          onSubmit={handleSubmit}
        >
          <div className="content-editor-grid">
            {resource.fields.map(
              (field) => {
                const value =
                  formValues[field.name];

                if (
                  field.type ===
                  "checkbox"
                ) {
                  return (
                    <label
                      className="content-checkbox-field"
                      key={field.name}
                    >
                      <input
                        type="checkbox"
                        checked={Boolean(
                          value,
                        )}
                        onChange={(
                          event,
                        ) => {
                          updateField(
                            field.name,
                            event.target
                              .checked,
                          );
                        }}
                      />

                      <span>
                        {field.label}
                      </span>
                    </label>
                  );
                }

                if (
                  field.type ===
                  "textarea" ||
                  field.type ===
                  "json" ||
                  field.type ===
                  "tags"
                ) {
                  return (
                    <label
                      className="content-field content-field-full"
                      key={field.name}
                    >
                      {field.label}

                      <textarea
                        required={
                          field.required
                        }
                        rows={
                          field.rows ??
                          (field.type ===
                          "json"
                            ? 7
                            : 4)
                        }
                        value={String(
                          value ?? "",
                        )}
                        placeholder={
                          field.placeholder
                        }
                        onChange={(
                          event,
                        ) => {
                          updateField(
                            field.name,
                            event.target
                              .value,
                          );
                        }}
                      />

                      {field.type ===
                        "tags" && (
                        <small>
                          Separate values
                          using commas.
                        </small>
                      )}

                      {field.type ===
                        "json" && (
                        <small>
                          Enter valid JSON
                          using double
                          quotation marks.
                        </small>
                      )}
                    </label>
                  );
                }

                if (
                  field.type === "select"
                ) {
                  return (
                    <label
                      className="content-field"
                      key={field.name}
                    >
                      {field.label}

                      <select
                        required={
                          field.required
                        }
                        value={String(
                          value ?? "",
                        )}
                        onChange={(
                          event,
                        ) => {
                          updateField(
                            field.name,
                            event.target
                              .value,
                          );
                        }}
                      >
                        <option value="">
                          Select
                        </option>

                        {field.options?.map(
                          (option) => (
                            <option
                              value={option}
                              key={option}
                            >
                              {option}
                            </option>
                          ),
                        )}
                      </select>
                    </label>
                  );
                }

                return (
                  <label
                    className="content-field"
                    key={field.name}
                  >
                    {field.label}

                    <input
                      required={
                        field.required
                      }
                      type={
                        field.type ===
                        "url"
                          ? "url"
                          : field.type
                      }
                      min={field.min}
                      max={field.max}
                      value={String(
                        value ?? "",
                      )}
                      placeholder={
                        field.placeholder
                      }
                      onChange={(
                        event,
                      ) => {
                        updateField(
                          field.name,
                          event.target
                            .value,
                        );
                      }}
                    />
                  </label>
                );
              },
            )}
          </div>

          {(formError || error) && (
            <div className="admin-alert admin-alert-error">
              {formError ?? error}
            </div>
          )}

          <div className="content-modal-actions">
            <button
              type="button"
              className="button button-secondary"
              onClick={onClose}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="button button-primary"
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

              Save Record
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}