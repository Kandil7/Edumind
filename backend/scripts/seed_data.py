"""
Seed database with demo content: Calculus course (Arabic).

Usage:
    cd backend
    python -m scripts.seed_data
"""
import asyncio
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import get_settings
from app.core.database import Base
from app.infrastructure.db.models.content import (
    ContentSourceModel, LessonModel, ConceptModel, SkillModel, ContentChunkModel,
)
from app.infrastructure.db.models.student import StudentModel

settings = get_settings()


LESSONS_DATA = [
    {
        "title": "مقدمة في المشتقات",
        "subject": "التفاضل والتكامل",
        "grade_level": "ثانوي",
        "language": "ar",
        "concepts": [
            {
                "name": "تعريف المشتقة",
                "description": "تعريف الميل الإنسياسي والمشتقة",
                "skills": ["حساب الميل الإنسياسي", "verständnisتعريف المشتقة"],
                "chunks": [
                    "المشتقة للدالة f(x) عند نقطة x=a هي الميل الإنسياسي لخط المماس عند تلك النقطة. تُكتب رياضياً كـ f'(a) = lim(h→0) [f(a+h) - f(a)] / h.",
                    "التعريف البديل للمشتقة: f'(x) = lim(Δx→0) Δy/Δx حيث Δy = f(x+Δx) - f(x).",
                ],
            },
            {
                "name": "قواعد التفاضل",
                "description": "قاعدة القوة، حاصل الضرب، حاصل القسمة",
                "skills": ["قاعدة القوة", "قاعدة الضرب", "قاعدة القسمة"],
                "chunks": [
                    "قاعدة القوة: إذا كانت f(x) = x^n فإن f'(x) = n·x^(n-1). هذه من أهم القواعد في التفاضل.",
                    "قاعدة الضرب: (fg)' = f'g + fg'. نستخدم هذه القاعدة عندما تكون الدالة حاصل ضرب دالتين.",
                    "قاعدة القسمة: (f/g)' = (f'g - fg') / g². نحتاج هذه القاعدة لتفاضل quotient.",
                ],
            },
            {
                "name": "الاشتقاق المتسلسل",
                "description": "اشتقاق الدوال المركبة",
                "skills": ["تطبيق قاعدة السلسلة"],
                "chunks": [
                    "قاعدة السلسلة: إذا كانت y = f(g(x)) فإن y' = f'(g(x)) · g'(x). هذه القاعدة أساسية للتفاضل.",
                    "مثال على قاعدة السلسلة: إذا كانت y = (2x+1)³ فإن y' = 3(2x+1)² · 2 = 6(2x+1)².",
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
                "description": "تحديد intervals الزيادة والنقصان والتقعر",
                "skills": ["تحليل الاتجاه", "تحليل التقعر"],
                "chunks": [
                    "الدالة تزداد عندما تكون f'(x) > 0 وتتناقص عندما تكون f'(x) < 0. نستخدم الجدول لتحديد الاتجاه.",
                    "الدالة مقعرة للأعلى عندما f''(x) > 0 ومقعرة للأسفل عندما f''(x) < 0.",
                ],
            },
            {
                "name": "ال extremum",
                "description": "القيم النهائية القصوى والصغرى",
                "skills": ["إيجاد extremum", "التحقق من extremum"],
                "chunks": [
                    "النقطة الحرجة هي حيث f'(x) = 0 أو f'(x) غير معرفة. لن 확인 هل هي extremum.",
                    "اختبار الجدول: نتحقق من تغيير إشارة f' حول النقطة الحرجة. تغير من موجب لسالب = قصوى، ومن سالب لموجب = صغرى.",
                ],
            },
        ],
    },
]


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Create demo student
        student_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
        student = StudentModel(
            id=student_id,
            name="طالب تجريبي",
            email="demo@edumind.com",
            preferred_language="ar",
            level="beginner",
        )
        session.add(student)

        for lesson_data in LESSONS_DATA:
            lesson_id = uuid.uuid4()
            lesson = LessonModel(
                id=lesson_id,
                title=lesson_data["title"],
                subject=lesson_data["subject"],
                grade_level=lesson_data["grade_level"],
                language=lesson_data["language"],
                description=f"درس {lesson_data['title']} في مادة {lesson_data['subject']}",
            )
            session.add(lesson)

            # Create a source for this lesson
            source_id = uuid.uuid4()
            source = ContentSourceModel(
                id=source_id,
                type="text",
                origin="teacher_upload",
                title=lesson_data["title"],
                language=lesson_data["language"],
                description=f"محتوى درس {lesson_data['title']}",
            )
            session.add(source)

            for concept_data in lesson_data["concepts"]:
                concept_id = uuid.uuid4()
                concept = ConceptModel(
                    id=concept_id,
                    lesson_id=lesson_id,
                    name=concept_data["name"],
                    description=concept_data["description"],
                )
                session.add(concept)

                for skill_name in concept_data["skills"]:
                    skill_id = uuid.uuid4()
                    skill = SkillModel(
                        id=skill_id,
                        concept_id=concept_id,
                        name=skill_name,
                    )
                    session.add(skill)

                    # Create content chunks for each skill
                    for i, chunk_text in enumerate(concept_data["chunks"]):
                        chunk = ContentChunkModel(
                            id=uuid.uuid4(),
                            source_id=source_id,
                            lesson_id=lesson_id,
                            concept_id=concept_id,
                            skill_id=skill_id,
                            content=chunk_text,
                            language=lesson_data["language"],
                            source_type="text",
                            start_offset=float(i * 500),
                            end_offset=float((i + 1) * 500),
                            metadata_={
                                "source_name": lesson_data["title"],
                                "concept_name": concept_data["name"],
                            },
                        )
                        session.add(chunk)

        await session.commit()
        print("Seeded successfully!")
        print(f"  - 1 demo student (demo@edumind.com)")
        print(f"  - {len(LESSONS_DATA)} lessons")
        print(f"  - {sum(len(l['concepts']) for l in LESSONS_DATA)} concepts")
        print(f"  - {sum(sum(len(c['skills']) for c in l['concepts']) for l in LESSONS_DATA)} skills")


if __name__ == "__main__":
    asyncio.run(seed())
