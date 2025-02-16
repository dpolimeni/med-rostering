from src.database.base import BaseDatabase
from src.users.models import UserInDB
import os
import json


class JsonDatabase(BaseDatabase):
    def __init__(self) -> None:
        self.client = None
        base_path = os.getcwd()
        self._db_name = os.path.join(base_path, "db.json")
        if not os.path.exists(self._db_name):
            with open(self._db_name, "w") as f:
                f.write("[]")

    async def get_client(self):
        # Verify if the database file exists
        with open(self._db_name, "r") as f:
            database = json.loads(f.read())
            self.client = database
        return

    async def get_user(self, mail: str) -> UserInDB:
        if self.client:
            for user in self.client:
                if user["email"] == mail:
                    return UserInDB(**user)
        return None

    async def create_user(self, user: UserInDB):
        if self.client is not None:
            print(user.model_dump())
            self.client.append(user.model_dump())
            with open(self._db_name, "w") as f:
                json.dump(self.client, f)
        return

    async def update_user(self, updated_user: UserInDB):
        if self.client:
            new_db = []
            for user in self.client:
                if user["email"] == updated_user.email:
                    user["hashed_password"] = updated_user.hashed_password
                    new_db.append(user)
                else:
                    new_db.append(user)
            with open(self._db_name, "w") as f:
                json.dump(self.client, f)

    async def verify_user(self, user_mail: str):
        if self.client:
            for user in self.client:
                if user["email"] == user_mail:
                    user["register_status"] = "active"
                    with open(self._db_name, "w") as f:
                        json.dump(self.client, f)
                    return
        return
