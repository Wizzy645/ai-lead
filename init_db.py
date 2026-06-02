# init_db.py
import sys
import asyncio

# Keep the Windows fix just in case Python needs it
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from database import engine, Base
import models


async def init_models():
    async with engine.begin() as conn:
        print("Creating database tables locally...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_models())
