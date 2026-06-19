"""Seed database with demo content: Calculus course (Arabic)."""
import asyncio
from uuid import uuid4 as _make_uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import get_settings
from app.core.database import Base
from app.infrastructure.db.models.content import (
    ContentSourceModel, LessonModel, ConceptModel, SkillModel, ContentChunkModel,
)
from app.infrastructure.db.models.student import StudentModel

settings = get_settings()

db_url = settings.effective_database_url
if "sqlite" in db_url and "aiosqlite" not in db_url:
    db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")

engine = create_async_engine(db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

LESSONS_DATA = [
    {
        "title": "مقدمة في المشتقات",
        "subject": "التفاضل والتكامل",
        "grade_level": "ثانوي",
        "language": "ar",
        "concepts": [
            {
                "name": "تعريف المشتقة",
                "skills": ["حساب الميل الإنسياسي", "تعريف المشتقة"],
                "chunks": [
                    "المشتقة للدالة f(x) عند نقطة x=a هي الميل الإنسياسي لخط المماس عند تلك النقطة. تُكتب f'(a) = lim(h→0) [f(a+h) - f(a)] / h.",
                    "التعريف البديل: f'(x) = lim(Δx→0) Δy/Δx حيث Δy = f(x+Δx) - f(x).",
                ],
            },
            {
                "name": "قواعد التفاضل",
                "skills": ["قاعدة القوة", "قاعدة الضرب", "قاعدة القسمة"],
                "chunks": [
                    "قاعدة القوة: إذا f(x) = x^n فإن f'(x) = n·x^(n-1).",
                    "قاعدة الضرب: (fg)' = f'g + fg'. نستخدمها لتفاضل حاصل ضرب دالتين.",
                    "قاعدة القسمة: (f/g)' = (f'g - fg') / g².",
                ],
            },
            {
                "name": "الاشتقاق المتسلسل",
                "skills": ["تطبيق قاعدة السلسلة"],
                "chunks": [
                    "قاعدة السلسلة: إذا y = f(g(x)) فإن y' = f'(g(x)) · g'(x).",
                    "مثال: إذا y = (2x+1)³ فإن y' = 3(2x+1)² · 2 = 6(2x+1)².",
                ],
            },
        ],
    },
    {
        "title": "تطبيقات المشتقات",
        "subject": "التفاضل والتكامل",
        "grade_level": "ثانوي",
        "language": "ar",
        "concepts": [
            {
                "name": "الاتجاه والتقعر",
                "skills": ["تحليل الاتجاه", "تحليل التقعر"],
                "chunks": [
                    "الدالة تزداد عندما f'(x) > 0 وتتناقص عندما f'(x) < 0.",
                    "الدالة مقعرة للأعلى عندما f''(x) > 0 ومقعرة للأسفل عندما f''(x) < 0.",
                ],
            },
            {
                "name": "ال extremum",
                "skills": ["إيجاد extremum", "التحقق من extremum"],
                "chunks": [
                    "النقطة الحرجة هي حيث f'(x) = 0 أو f'(x) غير معرفة.",
                    "اختبار الجدول: تغيير إشارة f' من موجب لسالب = قصوى، ومن سالب لموجب = صغرى.",
                ],
            },
        ],
    },
]


def _uuid() -> str:
    return str(_make_uuid())


async def seed():
    async with async_session() as session:
        from sqlalchemy import select
        existing = await session.execute(
            select(StudentModel).where(StudentModel.email == "demo@edumind.com")
        )
        if existing.scalar_one_or_none():
            print("Already seeded. Skipping.")
            return

        student = StudentModel(
            id="00000000-0000-0000-0000-000000000001",
            name="طالب تجريبي",
            email="demo@edumind.com",
            preferred_language="ar",
            level="beginner",
        )
        session.add(student)

        for lesson_data in LESSONS_DATA:
            lesson_id = _uuid()
            lesson = LessonModel(
                id=lesson_id,
                title=lesson_data["title"],
                subject=lesson_data["subject"],
                grade_level=lesson_data["grade_level"],
                language=lesson_data["language"],
            )
            session.add(lesson)

            source_id = _uuid()
            source = ContentSourceModel(
                id=source_id,
                type="text",
                origin="teacher_upload",
                title=lesson_data["title"],
                language=lesson_data["language"],
            )
            session.add(source)

            for concept_data in lesson_data["concepts"]:
                concept_id = _uuid()
                concept = ConceptModel(
                    id=concept_id,
                    lesson_id=lesson_id,
                    name=concept_data["name"],
                )
                session.add(concept)

                for skill_name in concept_data["skills"]:
                    skill_id = _uuid()
                    skill = SkillModel(
                        id=skill_id,
                        concept_id=concept_id,
                        name=skill_name,
                    )
                    session.add(skill)

                    for i, chunk_text in enumerate(concept_data["chunks"]):
                        chunk = ContentChunkModel(
                            id=_uuid(),
                            source_id=source_id,
                            lesson_id=lesson_id,
                            concept_id=concept_id,
                            skill_id=skill_id,
                            content=chunk_text,
                            language=lesson_data["language"],
                            source_type="text",
                            start_offset=float(i * 500),
                            end_offset=float((i + 1) * 500),
                            metadata_={"source_name": lesson_data["title"]},
                        )
                        session.add(chunk)

        await session.commit()
        print("Seeded successfully!")
        print(f"  - 1 demo student (demo@edumind.com)")
        print(f"  - {len(LESSONS_DATA)} lessons")


if __name__ == "__main__":
    asyncio.run(seed())
