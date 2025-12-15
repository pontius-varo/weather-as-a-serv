import os
from notify_service import send_sms, send_email, format_message


def lambda_handler(event, context):
    target_location = os.environ.get("TARGET_LOCATION", "Miami, FL")

    weather = get_weather(target_location)
    summary = maybe_generate_summary(weather)

    message = format_message(weather, summary)

    sms_recipient = os.environ.get("SMS_RECIPIENT", "").strip()
    email_recipient = os.environ.get("EMAIL_RECIPIENT", "").strip()

    if sms_recipient:
        send_sms(sms_recipient, message)

    if email_recipient:
        sender_email = os.environ.get("SENDER_EMAIL", "").strip()
        if not sender_email:
            raise ValueError("SENDER_EMAIL must be set to send emails via SES.")
        send_email(sender_email, email_recipient, "Daily Weather Report", message)

    return {
        "ok": True,
        "location": target_location,
        "sent_sms": bool(sms_recipient),
        "sent_email": bool(email_recipient),
    }
