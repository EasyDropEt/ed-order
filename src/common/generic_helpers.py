import os
import uuid

from dotenv import load_dotenv

from src.common.typing.config import Config


def get_new_id() -> uuid.UUID:
    return uuid.uuid4()


def get_config() -> Config:
    load_dotenv()

    return {
        "mongo_db_connection_string": os.getenv("CONNECTION_STRING") or "",
        "db_name": os.getenv("DB_NAME") or "",
        "rabbitmq_url": os.getenv("RABBITMQ_URL") or "",
    }
