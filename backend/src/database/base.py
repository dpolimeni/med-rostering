from abc import ABC, abstractmethod
from .models import UserInDB


class BaseDatabase(ABC):
    @abstractmethod
    async def get_client(self):
        pass

    @abstractmethod
    async def get_user(self, mail: str) -> UserInDB:
        pass

    @abstractmethod
    async def create_user(self, user: UserInDB):
        pass

    @abstractmethod
    async def update_user(self, updated_user: UserInDB):
        pass

    @abstractmethod
    async def verify_user(self, user_mail: str):
        pass
