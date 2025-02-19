from abc import ABC, abstractmethod

from src.department.models import Department
from src.specialization.models import Specialization
from src.users.models import UserInDB


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

    @abstractmethod
    async def get_specialization(self, specialization_id: str):
        pass

    @abstractmethod
    async def create_specialization(
        self, specialization: Specialization, user: UserInDB
    ):
        """Create a new specialization and add its id to the user collection.

        Args:
            specialization (Specialization): Specialization Db object
            user (UserInDB): User Db object
        """
        pass

    @abstractmethod
    async def update_specialization(self, specialization: Specialization):
        pass

    @abstractmethod
    async def get_department(self, department_id: str):
        pass

    @abstractmethod
    async def create_department(
        self, department: Department, specialization: Specialization
    ):
        pass

    @abstractmethod
    async def update_department(self, department: Department):
        pass
