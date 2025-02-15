from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from .templates import RESET_PASSWORD
from .schemas import UserLoginRegister, RequestPasswordReset, ResetPassword, GoogleLogin
from .utils import PasswordHasher, TokenManager, EmailSender, send_verification_email
from src.database.models import UserInDB
from src.database.nosql.json_db import JsonDatabase
from src.database.factory import get_session
from src.settings import app_settings


router = APIRouter(prefix="/auth", tags=["auth"])
db_client = Annotated[JsonDatabase, Depends(get_session)]


@router.post("/register")
async def register(
    user: UserLoginRegister, database: db_client, background_tasks: BackgroundTasks
):
    db_user = await database.get_user(user.email)
    if db_user and db_user.register_status == "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    manager = PasswordHasher()
    hashed_password = manager.hash_password(user.password)
    user = UserInDB(
        email=user.email, hashed_password=hashed_password, register_status="pending"
    )

    background_tasks.add_task(send_verification_email, user)
    await database.create_user(user)
    return {"message": "User registered"}


@router.post("/login")
async def login(user: UserLoginRegister, database: db_client):
    db_user = await database.get_user(user.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    if db_user.register_status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not verified"
        )

    manager = PasswordHasher()
    if not manager.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Generate JWT token
    jwt_manager = TokenManager(app_settings.JWT_SECRET_KEY)
    access_token, refresh_token = jwt_manager.create_tokens(db_user)

    return JSONResponse(
        {"access": access_token, "refresh": refresh_token},
        status_code=status.HTTP_200_OK,
    )


@router.post("/login/google")
async def google_login_register(google_login: GoogleLogin, database: db_client):
    """
    Login or register a user with Google.

    Args:
        id_token (str): The Google ID token obtained from the client-side.
    """
    try:
        # Verify Google ID token
        idinfo = google_id_token.verify_oauth2_token(
            google_login.id_token,
            google_requests.Request(),
            app_settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10,
        )

        if idinfo["email"] != google_login.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
            )

        # Check if user exists
        user = await database.get_user(idinfo["email"])
        if not user:
            # Register user
            user = UserInDB(email=idinfo["email"], register_status="active")
            await database.create_user(user)

        # Obtain tokens
        jwt_manager = TokenManager(app_settings.JWT_SECRET_KEY)
        access_token, refresh_token = jwt_manager.create_tokens(user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    return JSONResponse(
        {"access": access_token, "refresh": refresh_token},
        status_code=status.HTTP_200_OK,
    )


@router.get("/refresh")
async def refresh_token(refresh_token: str):
    jwt_manager = TokenManager(app_settings.JWT_SECRET_KEY)
    access_token = jwt_manager.refresh_tokens(refresh_token)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    return JSONResponse({"access": access_token}, status_code=status.HTTP_200_OK)


# API endpoints
@router.post("/request-password-reset")
async def request_password_reset(request: RequestPasswordReset, database: db_client):
    """
    Initiates the password reset process by sending a reset link to the user's email.
    """
    user = await database.get_user(request.email)
    if not user:
        # Don't reveal whether the email exists
        return {"message": "If the email exists, a password reset link will be sent"}

    # Generate password reset token
    token = TokenManager.create_token(
        {"sub": user.email, "type": "password_reset"},
        timedelta(minutes=app_settings.RESET_TOKEN_EXPIRE_MINUTES),
        app_settings.JWT_SECRET_KEY,
    )

    # Create password reset link
    reset_link = f"{app_settings.BASE_URL}/reset-password?token={token}"

    # Email template
    html_content = RESET_PASSWORD.format(
        reset_link=reset_link, expire=app_settings.RESET_TOKEN_EXPIRE_MINUTES
    )

    # Send email
    EmailSender.send_email(
        to_email=request.email,
        subject="Password Reset Request",
        html_content=html_content,
    )

    return {"message": "If the email exists, a password reset link will be sent"}


@router.post("/reset-password")
async def reset_password(reset_data: ResetPassword, database: db_client):
    """
    Resets the user's password using the provided token.
    """
    # Verify token
    payload = TokenManager.verify_token(reset_data.token)

    if payload.get("type") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type"
        )

    # Hash new password
    hashed_password = PasswordHasher().hash_password(reset_data.new_password)

    user = await database.get_user(payload.get("email"))
    user.hashed_password = hashed_password

    # Update password in database
    await database.update_user(user)

    return {"message": "Password has been reset successfully"}


@router.post("/verify-email")
async def verify_email(token: str, database: db_client):
    """
    Verifies the user's email address using the provided token.
    """
    # Verify token
    payload = TokenManager().verify_token(token, "email_verification")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    user = await database.get_user(payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    if user.register_status == "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    # Update user's email verification status
    await database.verify_user(payload.get("sub"))

    return {"message": "Email verified successfully"}


#
#
# # Utility endpoint to send verification email (typically called after registration)
# @router.post("/send-verification-email")
# async def send_verification_email(user_id: str, email: EmailStr):
#     """
#     Sends an email verification link to the user.
#     """
#     # Generate email verification token
#     token = TokenManager.create_token(
#         {"sub": user_id, "type": "email_verification"},
#         timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES),
#     )
#
#     # Create verification link
#     verification_link = f"{BASE_URL}/verify-email?token={token}"
#
#     # Email template
#     html_content = f"""
#     <html>
#         <body>
#             <h2>Verify Your Email</h2>
#             <p>Click the link below to verify your email address. This link will expire in 24 hours.</p>
#             <p><a href="{verification_link}">Verify Email</a></p>
#         </body>
#     </html>
#     """
#
#     # Send email
#     EmailSender.send_email(
#         to_email=email, subject="Verify Your Email", html_content=html_content
#     )
#
#     return {"message": "Verification email sent"}
#
