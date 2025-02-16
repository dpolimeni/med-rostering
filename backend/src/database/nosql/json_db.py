from src.database.base import BaseDatabase
from src.users.models import UserInDB
from src.specialization.models import Specialization
import os
import json


class JsonDatabase(BaseDatabase):
    def __init__(self) -> None:
        self.user_client = None
        self.specialization_client = None
        base_path = os.getcwd()
        self._users_collection = os.path.join(base_path, "users_db.json")
        self._specialization_collection = os.path.join(
            base_path, "specialization_db.json"
        )
        if not os.path.exists(self._users_collection):
            with open(self._users_collection, "w") as f:
                f.write("[]")

    async def get_client(self):
        # Verify if the database file exists
        with open(self._users_collection, "r") as f:
            database = json.loads(f.read())
            self.user_client = database

        with open(self._specialization_collection, "r") as f:
            database = json.loads(f.read())
            self.specialization_client = database
        return

    async def get_user(self, mail: str) -> UserInDB:
        if self.user_client:
            for user in self.user_client:
                if user["email"] == mail:
                    return UserInDB(**user)
        return None

    async def create_user(self, user: UserInDB):
        if self.user_client is not None:
            print(user.model_dump())
            self.user_client.append(user.model_dump())
            with open(self._users_collection, "w") as f:
                json.dump(self.user_client, f)
        return

    async def update_user(self, updated_user: UserInDB):
        if self.user_client:
            new_db = []
            for user in self.user_client:
                if user["email"] == updated_user.email:
                    user["hashed_password"] = updated_user.hashed_password
                    new_db.append(user)
                else:
                    new_db.append(user)
            with open(self._users_collection, "w") as f:
                json.dump(self.user_client, f)

    async def verify_user(self, user_mail: str):
        if self.user_client:
            for user in self.user_client:
                if user["email"] == user_mail:
                    user["register_status"] = "active"
                    with open(self._users_collection, "w") as f:
                        json.dump(self.user_client, f)
                    return
        return

    async def get_specialization(self, specialization_id: str) -> Specialization:
        if self.specialization_client:
            for specialization in self.specialization_client:
                if specialization["id"] == specialization_id:
                    return Specialization(**specialization)
        return None
    
    async def create_specialization(self, specialization: Specialization):
        if self.specialization_client is not None:
            self.specialization_client.append(specialization.model_dump())
            with open(self._specialization_collection, "w") as f:
                json.dump(self.specialization_client, f)
        return
