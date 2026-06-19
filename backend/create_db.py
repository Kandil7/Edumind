import asyncio
from app.core.database import engine, Base
from app.infrastructure.db.models import *  # noqa

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

asyncio.run(main())
