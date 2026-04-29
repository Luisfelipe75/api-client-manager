from datetime import datetime, timezone
from db.collections import CollectionNames

async def create_session(db, token: str, userid: str, username: str):
    doc = {
        "token": token,
        "userid": userid,
        "username": username,
        "login_timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db[CollectionNames.SESIONES].insert_one(doc)
    return doc


async def delete_session(db, userid: str):
    await db[CollectionNames.SESIONES].delete_one({"userid": userid})


async def get_session_by_token(db, token: str):
    return await db[CollectionNames.SESIONES].find_one({"token": token})
