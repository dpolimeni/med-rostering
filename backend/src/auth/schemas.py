from pydantic import BaseModel


class UserLoginRegister(BaseModel):
    email: str
    password: str


class GoogleLogin(BaseModel):
    email: str
    id_token: str


class RequestPasswordReset(BaseModel):
    email: str  # EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str


class VerifyEmail(BaseModel):
    token: str
