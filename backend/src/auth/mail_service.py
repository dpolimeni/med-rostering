from datetime import timedelta

from fastapi import HTTPException, status
from sendgrid import Mail, SendGridAPIClient
from src.auth.mail_templates import CONFIRM_REGISTRATION
from src.auth.utils import TokenManager
from src.settings import app_settings
from src.users.models import UserInDB


# Email sender
class EmailSender:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str):
        message = Mail(
            from_email=app_settings.SENDGRID_SENDER,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )

        try:
            sg = SendGridAPIClient(app_settings.SENDGRID_API_KEY)
            response = sg.send(message)
            if response.status_code not in (200, 202):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send email via SendGrid",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send email: {str(e)}",
            )


async def send_verification_email(user: UserInDB):
    token = TokenManager.create_token(
        {"sub": user.email, "type": "email_verification"},
        timedelta(minutes=app_settings.EMAIL_TOKEN_EXPIRE_MINUTES),
        app_settings.JWT_SECRET_KEY,
    )
    html_content = CONFIRM_REGISTRATION.format(
        confirm_link=f"{app_settings.BASE_URL}/register?token={token}",
        expire=app_settings.EMAIL_TOKEN_EXPIRE_MINUTES,
    )
    EmailSender.send_email(
        to_email=user.email,
        subject="Confirm Registration",
        html_content=html_content,
    )
