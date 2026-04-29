from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_mongo():
    db_instance.client = AsyncIOMotorClient(settings.mongodb_uri)
    db_instance.db = db_instance.client[settings.mongodb_db]

async def close_mongo():
    if db_instance.client:
        db_instance.client.close()

def get_db():
    return db_instance.db