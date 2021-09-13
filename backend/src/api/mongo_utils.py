import logging

from motor.motor_asyncio import AsyncIOMotorClient

from ..dinnerme.settings import MongoDB as MongoDBSettings  # type: ignore
from .shared import db


async def connect_to_mongo() -> None:
    logging.info(f"connecting to mongo..., {MongoDBSettings.conn_string}")
    db.client = AsyncIOMotorClient(MongoDBSettings.conn_string)
    db.menu = db.client.client.menu
    logging.info("connected to menu collection")


async def close_mongo_connection() -> None:
    logging.info("closing connection...")
    db.client.close()
    logging.info("closed connection")
