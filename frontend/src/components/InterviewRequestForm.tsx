import {
  CalendarDays,
  CheckCircle2,
  LoaderCircle,
  Send,
} from "lucide-react";
import {
  type FormEvent,
  useState,
} from "react";

import { publicApi } from "../lib/api";

interface InterviewFormState {
  name: string;
  email: string;
  phone: string;
  company: string;
  role: string;
  preferredDatetime: string;
  timezone: string;
  meetingMode: string;
  message: string;
}

const initialFormState: InterviewFormState = {
  name: "",
  email: "",
  phone: "",
  company: "",
  role: "",
  preferredDatetime: "",
  timezone: "Asia/Kolkata",
  meetingMode: "Google Meet",
  message: "",
};

export default function InterviewRequestForm() {
  const [form, setForm] =
    useState<InterviewFormState>(
      initialFormState,
    );

  const [submitting, setSubmitting] =
    useState(false);

  const [successMessage, setSuccessMessage] =
    useState<string | null>(null);

  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);

  function updateField(
    field: keyof InterviewFormState,
    value: string,
  ) {
    setForm((currentForm) => ({
      ...currentForm,
      [field]: value,
    }));
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setSubmitting(true);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      let preferredDatetime: string | null =
        null;

      if (form.preferredDatetime) {
        const selectedDate = new Date(
          form.preferredDatetime,
        );

        if (
          Number.isNaN(
            selectedDate.getTime(),
          )
        ) {
          throw new Error(
            "Please select a valid interview date and time.",
          );
        }

        preferredDatetime =
          selectedDate.toISOString();
      }

      const response =
        await publicApi.submitInterviewRequest({
          name: form.name.trim(),
          email: form.email.trim(),
          phone:
            form.phone.trim() || null,
          company: form.company.trim(),
          role: form.role.trim(),
          preferred_datetime:
            preferredDatetime,
          timezone:
            form.timezone.trim() || null,
          meeting_mode:
            form.meetingMode.trim() || null,
          message:
            form.message.trim() || null,
        });

      setSuccessMessage(response.message);
      setForm(initialFormState);
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Could not submit the interview request.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      className="ai-form interview-request-form"
      onSubmit={handleSubmit}
    >
      <div className="ai-form-heading">
        <span className="ai-form-icon">
          <CalendarDays size={24} />
        </span>

        <div>
          <h3>Request an Interview</h3>

          <p>
            Submit an interview request for a
            software, AI/ML, research or academic
            opportunity.
          </p>
        </div>
      </div>

      <div className="ai-form-grid">
        <label>
          Your Name
          <input
            required
            minLength={2}
            maxLength={150}
            value={form.name}
            onChange={(event) => {
              updateField(
                "name",
                event.target.value,
              );
            }}
            placeholder="Recruiter or hiring manager"
          />
        </label>

        <label>
          Email
          <input
            required
            type="email"
            value={form.email}
            onChange={(event) => {
              updateField(
                "email",
                event.target.value,
              );
            }}
            placeholder="you@company.com"
          />
        </label>

        <label>
          Phone
          <input
            maxLength={30}
            value={form.phone}
            onChange={(event) => {
              updateField(
                "phone",
                event.target.value,
              );
            }}
            placeholder="Optional"
          />
        </label>

        <label>
          Company
          <input
            required
            minLength={2}
            maxLength={200}
            value={form.company}
            onChange={(event) => {
              updateField(
                "company",
                event.target.value,
              );
            }}
            placeholder="Company or institution"
          />
        </label>

        <label>
          Role
          <input
            required
            minLength={2}
            maxLength={200}
            value={form.role}
            onChange={(event) => {
              updateField(
                "role",
                event.target.value,
              );
            }}
            placeholder="Python Backend Developer"
          />
        </label>

        <label>
          Preferred Date and Time
          <input
            type="datetime-local"
            value={form.preferredDatetime}
            onChange={(event) => {
              updateField(
                "preferredDatetime",
                event.target.value,
              );
            }}
          />
        </label>

        <label>
          Timezone
          <input
            maxLength={100}
            value={form.timezone}
            onChange={(event) => {
              updateField(
                "timezone",
                event.target.value,
              );
            }}
            placeholder="Asia/Kolkata"
          />
        </label>

        <label>
          Meeting Mode
          <select
            value={form.meetingMode}
            onChange={(event) => {
              updateField(
                "meetingMode",
                event.target.value,
              );
            }}
          >
            <option value="Google Meet">
              Google Meet
            </option>

            <option value="Microsoft Teams">
              Microsoft Teams
            </option>

            <option value="Zoom">
              Zoom
            </option>

            <option value="Phone">
              Phone
            </option>

            <option value="In Person">
              In Person
            </option>
          </select>
        </label>
      </div>

      <label>
        Message
        <textarea
          rows={5}
          maxLength={5000}
          value={form.message}
          onChange={(event) => {
            updateField(
              "message",
              event.target.value,
            );
          }}
          placeholder="Add interview details, responsibilities or other information."
        />
      </label>

      {successMessage && (
        <div className="ai-form-message ai-form-success">
          <CheckCircle2 size={18} />
          {successMessage}
        </div>
      )}

      {errorMessage && (
        <div className="ai-form-message ai-form-error">
          {errorMessage}
        </div>
      )}

      <button
        className="button button-primary button-full"
        type="submit"
        disabled={submitting}
      >
        {submitting ? (
          <>
            <LoaderCircle
              className="spin"
              size={18}
            />
            Submitting
          </>
        ) : (
          <>
            <Send size={18} />
            Submit Interview Request
          </>
        )}
      </button>
    </form>
  );
}