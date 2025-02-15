from src.database.nosql.json_db import JsonDatabase
from src.settings import app_settings


async def get_session():
    db_type = app_settings.DB_TYPE

    if db_type == "json":
        db = JsonDatabase()
        await db.get_client()
        return db
    else:
        raise ValueError("Invalid database type")
