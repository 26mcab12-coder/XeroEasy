import os
import smtplib
import ssl
from email.message import EmailMessage


class EmailNotificationError(Exception):
    """Raised when SMTP is configured but an email cannot be delivered."""


def send_order_completed_email(recipient, student_name, order_id):
    if not recipient or not recipient.strip():
        raise EmailNotificationError("The student account has no email address.")

    host = os.getenv("XEROEASY_SMTP_HOST", "").strip()
    sender = os.getenv("XEROEASY_SMTP_FROM", "").strip()
    if not host or not sender:
        return "not_configured"

    try:
        port = int(os.getenv("XEROEASY_SMTP_PORT", "587"))
    except ValueError as error:
        raise EmailNotificationError("XEROEASY_SMTP_PORT must be a valid port number.") from error

    if not 1 <= port <= 65535:
        raise EmailNotificationError("XEROEASY_SMTP_PORT must be between 1 and 65535.")

    username = os.getenv("XEROEASY_SMTP_USERNAME", "")
    password = os.getenv("XEROEASY_SMTP_PASSWORD", "")
    if bool(username) != bool(password):
        raise EmailNotificationError(
            "Set both XEROEASY_SMTP_USERNAME and XEROEASY_SMTP_PASSWORD, or leave both unset."
        )

    use_ssl = os.getenv("XEROEASY_SMTP_USE_SSL", "false").strip().lower() in {"1", "true", "yes"}
    use_tls = os.getenv("XEROEASY_SMTP_USE_TLS", "true").strip().lower() in {"1", "true", "yes"}
    if use_ssl and use_tls:
        raise EmailNotificationError("Enable either SMTP SSL or STARTTLS, not both.")

    try:
        message = EmailMessage()
        message["Subject"] = f"Your XeroEasy order #XE-{order_id} is ready"
        message["From"] = sender
        message["To"] = recipient
        message.set_content(
            f"""Hello {student_name},

Your XeroEasy print order #XE-{order_id} has been completed and is ready for collection.

Please visit your selected campus collection point to collect it.

Thank you,
XeroEasy Copy Centre
"""
        )
    except (TypeError, ValueError) as error:
        raise EmailNotificationError("The completion email contains an invalid address or message value.") from error

    try:
        if use_ssl:
            with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=20) as smtp:
                if username:
                    smtp.login(username, password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=20) as smtp:
                if use_tls:
                    smtp.starttls(context=ssl.create_default_context())
                if username:
                    smtp.login(username, password)
                smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        raise EmailNotificationError("The completion email could not be delivered.") from error

    return "sent"
