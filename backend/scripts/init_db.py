"""Create all database tables from ORM models."""
import asyncio
from app.core.database import engine, Base
# Import all models to register them with Base
from app.infrastructure.db.models import content, student, question, misconception  # noqa

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(main())
