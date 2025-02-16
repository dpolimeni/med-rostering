from fastapi import HTTPException, Request, status
from src.auth.services.token import TokenManager
from src.database.factory import get_session
from src.users.models import UserInDB


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
