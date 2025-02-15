from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple, Optional
from uuid import uuid4

import jwt
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from sendgrid import SendGridAPIClient, Mail
from src.auth.templates import CONFIRM_REGISTRATION
from src.database.factory import get_session
from src.database.models import UserInDB
from src.settings import app_settings


class PasswordHasher:
    def __init__(self, rounds: int = 12):
        """Initialize the password hasher with bcrypt.

        Args:
            rounds: Number of rounds for bcrypt (default=12)
        """
        # Configure the password context with bcrypt
        self.pwd_context = CryptContext(
            schemes=["bcrypt"], default="bcrypt", bcrypt__default_rounds=rounds
        )

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: The plain-text password to hash

        Returns:
            str: The hashed password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain-text password to verify
            hashed_password: The hashed password to check against

        Returns:
            bool: True if the password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def need_rehash(self, hashed_password: str) -> bool:
        """Check if a password needs to be rehashed.

        Useful when you want to upgrade security parameters.

        Args:
            hashed_password: The hashed password to check

        Returns:
            bool: True if the password should be rehashed
        """
        return self.pwd_context.needs_update(hashed_password)


class TokenManager:
    def __init__(
        self,
        access_token_secret: str = app_settings.JWT_SECRET_KEY,
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7,
    ):
        """Initialize the token manager.

        Args:
            access_token_secret: Secret key for access tokens
            refresh_token_secret: Secret key for refresh tokens
            access_token_expire_minutes: Access token lifetime in minutes
            refresh_token_expire_days: Refresh token lifetime in days
        """
        self.token_secret = access_token_secret
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    @staticmethod
    def create_token(
        data: dict,
        expires_delta: timedelta,
        token_secret: str,
        algorithm: str = "HS256",
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, token_secret, algorithm=algorithm)
        return encoded_jwt

    def _generate_token(
        self,
        user_data: UserInDB,
        token_type: str,
        expires_delta: timedelta,
        secret_key: str,
    ) -> str:
        """Generate a JWT token.

        Args:
            user_data: UserInDB information to encode in the token
            token_type: Type of token (access or refresh)
            expires_delta: Token expiration time
            secret_key: Secret key for signing the token

        Returns:
            str: Generated JWT token
        """

        expire = datetime.now(timezone.utc) + expires_delta

        if token_type == "access":
            payload = {
                "sub": user_data.email,
                "roles": user_data.roles,
                "exp": expire,
                "type": token_type,
            }
        else:
            payload = {
                "sub": user_data.email,
                "roles": user_data.roles,
                "exp": expire,
                "jti": str(uuid4()),
                "type": token_type,
            }

        return jwt.encode(payload, secret_key, algorithm="HS256")

    def create_tokens(self, user_data: UserInDB) -> Tuple[str, str]:
        """Create both access and refresh tokens.

        Args:
            user_data: User information to encode in the tokens

        Returns:
            Tuple[str, str]: Access token and refresh token
        """
        # Create access token
        access_token = self._generate_token(
            user_data=user_data,
            token_type="access",
            expires_delta=timedelta(seconds=self.access_token_expire_minutes),
            secret_key=self.token_secret,
        )

        # Create refresh token
        refresh_token = self._generate_token(
            user_data=user_data,
            token_type="refresh",
            expires_delta=timedelta(days=self.refresh_token_expire_days),
            secret_key=self.token_secret,
        )

        return access_token, refresh_token

    def verify_token(self, token: str, token_type: str = "") -> Optional[Dict]:
        """Verify a token and return its payload if valid.

        Args:
            token: Token to verify
            token_type: Type of token (access or refresh)

        Returns:
            Optional[Dict]: Token payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.token_secret, algorithms=["HS256"])

            # Verify token type
            if payload.get("type") != token_type:
                return None

            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Create new access and refresh tokens using a valid refresh token.

        Args:
            refresh_token: Current refresh token

        Returns:
            Optional[Tuple[str, str]]: New access and refresh tokens if valid,
                                     None if invalid
        """
        # Verify the refresh token
        payload = self.verify_token(refresh_token, "refresh")
        if not payload:
            return None

        # Remove token-specific claims for new tokens
        user_data = payload.copy()
        for claim in ["exp", "iat", "jti", "type"]:
            user_data.pop(claim, None)

        # Create new tokens
        return self.create_tokens(
            UserInDB(email=user_data["sub"], roles=user_data["roles"])
        )[0]


async def get_current_user(request: Request) -> UserInDB | None:
    """Get the current user from the request.

    Args:
        request: Incoming request

    Returns:
        User: The current user
    """
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = token.split("Bearer ")[-1]
    manager = TokenManager()
    payload = manager.verify_token(token, "access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = payload["sub"]
    database = await get_session()
    user = await database.get_user(user_id)
    if not user or user.register_status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


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
