import databases
from datetime import datetime
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)

DATABASE_URL = "sqlite:///./my.db"
database = databases.Database(DATABASE_URL)

metadata = MetaData()

webhook_events = Table(
    "webhook_events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("commit_hash", String),
    Column("commit_message", String),
    Column("datetime", DateTime),
    Column("logs", String),
    Column("success", Boolean),
    Column("name", String),  # Should be "format" or "test"
)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


async def insert_webhook_event(
    commit_hash: str,
    commit_message: str,
    datetime: datetime,
    logs: str,
    success: bool,
    name: str,
):
    query = webhook_events.insert().values(
        commit_hash=commit_hash,
        commit_message=commit_message,
        datetime=datetime,
        logs=logs,
        success=success,
        name=name,
    )
    last_record_id = await database.execute(query)
    return last_record_id
