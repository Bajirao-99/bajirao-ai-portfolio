import html
import logging
from typing import Any

import resend

from app.core.config import settings


logger = logging.getLogger(__name__)


def email_notifications_available() -> bool:
    return bool(
        settings.email_notifications_enabled
        and settings.resend_api_key
        and settings.email_from_address
        and settings.admin_notification_email
    )


def get_sender() -> str:
    return (
        f"{settings.email_from_name} "
        f"<{settings.email_from_address}>"
    )


def send_email(
    *,
    to: list[str],
    subject: str,
    html_content: str,
) -> str | None:
    if not email_notifications_available():
        logger.info(
            "Email notification skipped because "
            "email notifications are disabled."
        )
        return None

    try:
        resend.api_key = (
            settings.resend_api_key
        )

        parameters: resend.Emails.SendParams = {
            "from": get_sender(),
            "to": to,
            "subject": subject,
            "html": html_content,
        }

        response: Any = resend.Emails.send(
            parameters
        )

        if isinstance(response, dict):
            return str(
                response.get("id", "")
            ) or None

        return str(response)

    except Exception:
        logger.exception(
            "Email delivery failed. "
            "Subject=%s",
            subject,
        )

        return None


def send_contact_admin_notification(
    *,
    name: str,
    email: str,
    phone: str | None,
    subject: str,
    message: str,
) -> str | None:
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_phone = html.escape(
        phone or "Not provided"
    )
    safe_subject = html.escape(subject)
    safe_message = html.escape(
        message
    ).replace("\n", "<br />")

    email_html = f"""
    <div style="
        font-family:Arial,sans-serif;
        max-width:680px;
        margin:auto;
        color:#26343d;
    ">
        <h2 style="color:#9b382e;">
            New Portfolio Contact Message
        </h2>

        <p>
            A visitor submitted a message
            through your portfolio.
        </p>

        <table style="
            width:100%;
            border-collapse:collapse;
        ">
            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Name
                </td>
                <td style="padding:8px;">
                    {safe_name}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Email
                </td>
                <td style="padding:8px;">
                    {safe_email}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Phone
                </td>
                <td style="padding:8px;">
                    {safe_phone}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Subject
                </td>
                <td style="padding:8px;">
                    {safe_subject}
                </td>
            </tr>
        </table>

        <div style="
            margin-top:20px;
            padding:16px;
            background:#f6f3f0;
            border-radius:10px;
        ">
            {safe_message}
        </div>

        <p style="margin-top:22px;">
            <a
                href="{settings.public_frontend_url}/admin/messages"
                style="
                    display:inline-block;
                    padding:11px 16px;
                    color:white;
                    background:#9b382e;
                    text-decoration:none;
                    border-radius:8px;
                "
            >
                Open Admin Messages
            </a>
        </p>
    </div>
    """

    return send_email(
        to=[
            settings.admin_notification_email
        ],
        subject=(
            f"Portfolio contact: {subject}"
        ),
        html_content=email_html,
    )


def send_contact_confirmation(
    *,
    name: str,
    email: str,
    subject: str,
) -> str | None:
    safe_name = html.escape(name)
    safe_subject = html.escape(subject)

    email_html = f"""
    <div style="
        font-family:Arial,sans-serif;
        max-width:650px;
        margin:auto;
        color:#26343d;
    ">
        <h2 style="color:#9b382e;">
            Thank you for contacting me
        </h2>

        <p>Hello {safe_name},</p>

        <p>
            Your message regarding
            <strong>{safe_subject}</strong>
            has been received successfully.
        </p>

        <p>
            I will review the message and
            respond as soon as possible.
        </p>

        <p>
            Regards,<br />
            <strong>
                Bajirao Ramling Salunke
            </strong>
        </p>

        <p>
            <a href="{settings.public_frontend_url}">
                Visit the portfolio
            </a>
        </p>
    </div>
    """

    return send_email(
        to=[email],
        subject=(
            "Your portfolio message was received"
        ),
        html_content=email_html,
    )


def send_interview_admin_notification(
    *,
    name: str,
    email: str,
    phone: str | None,
    company: str,
    role: str,
    preferred_datetime: str | None,
    timezone: str | None,
    meeting_mode: str | None,
    message: str | None,
) -> str | None:
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_phone = html.escape(
        phone or "Not provided"
    )
    safe_company = html.escape(company)
    safe_role = html.escape(role)
    safe_datetime = html.escape(
        preferred_datetime or "Not specified"
    )
    safe_timezone = html.escape(
        timezone or "Not specified"
    )
    safe_mode = html.escape(
        meeting_mode or "Not specified"
    )
    safe_message = html.escape(
        message or "No additional message"
    ).replace("\n", "<br />")

    email_html = f"""
    <div style="
        font-family:Arial,sans-serif;
        max-width:680px;
        margin:auto;
        color:#26343d;
    ">
        <h2 style="color:#9b382e;">
            New Interview Request
        </h2>

        <p>
            A recruiter submitted an interview
            request through your portfolio.
        </p>

        <table style="
            width:100%;
            border-collapse:collapse;
        ">
            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Recruiter
                </td>
                <td style="padding:8px;">
                    {safe_name}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Email
                </td>
                <td style="padding:8px;">
                    {safe_email}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Phone
                </td>
                <td style="padding:8px;">
                    {safe_phone}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Company
                </td>
                <td style="padding:8px;">
                    {safe_company}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Role
                </td>
                <td style="padding:8px;">
                    {safe_role}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Preferred time
                </td>
                <td style="padding:8px;">
                    {safe_datetime}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Timezone
                </td>
                <td style="padding:8px;">
                    {safe_timezone}
                </td>
            </tr>

            <tr>
                <td style="padding:8px;font-weight:bold;">
                    Meeting mode
                </td>
                <td style="padding:8px;">
                    {safe_mode}
                </td>
            </tr>
        </table>

        <div style="
            margin-top:20px;
            padding:16px;
            background:#f6f3f0;
            border-radius:10px;
        ">
            {safe_message}
        </div>

        <p style="margin-top:22px;">
            <a
                href="{settings.public_frontend_url}/admin/interviews"
                style="
                    display:inline-block;
                    padding:11px 16px;
                    color:white;
                    background:#9b382e;
                    text-decoration:none;
                    border-radius:8px;
                "
            >
                Open Interview Requests
            </a>
        </p>
    </div>
    """

    return send_email(
        to=[
            settings.admin_notification_email
        ],
        subject=(
            f"Interview request: "
            f"{safe_role} at {safe_company}"
        ),
        html_content=email_html,
    )


def send_interview_confirmation(
    *,
    name: str,
    email: str,
    company: str,
    role: str,
) -> str | None:
    safe_name = html.escape(name)
    safe_company = html.escape(company)
    safe_role = html.escape(role)

    email_html = f"""
    <div style="
        font-family:Arial,sans-serif;
        max-width:650px;
        margin:auto;
        color:#26343d;
    ">
        <h2 style="color:#9b382e;">
            Interview request received
        </h2>

        <p>Hello {safe_name},</p>

        <p>
            Your interview request for the
            <strong>{safe_role}</strong> role
            at <strong>{safe_company}</strong>
            was received successfully.
        </p>

        <p>
            I will review the proposed details
            and contact you using the email
            address provided.
        </p>

        <p>
            Regards,<br />
            <strong>
                Bajirao Ramling Salunke
            </strong>
        </p>
    </div>
    """

    return send_email(
        to=[email],
        subject=(
            "Your interview request was received"
        ),
        html_content=email_html,
    )


def send_test_email() -> str | None:
    return send_email(
        to=[
            settings.admin_notification_email
        ],
        subject=(
            "Bajirao Portfolio email test"
        ),
        html_content=(
            "<h2>Email notifications work.</h2>"
            "<p>Your production email "
            "configuration is valid.</p>"
        ),
    )