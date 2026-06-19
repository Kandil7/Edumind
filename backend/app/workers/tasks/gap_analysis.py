from app.workers.celery_app import celery_app


@celery_app.task(bind=True, name="gap_analysis.analyze_skill")
def analyze_skill_gaps_task(self, skill_id: str):
    """
    Background task to analyze misconceptions for a skill.
    Clusters wrong answer patterns and creates/updates misconceptions.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from uuid import UUID
    from app.core.config import get_settings

    settings = get_settings()
    engine = create_engine(settings.SYNC_DATABASE_URL)

    with Session(engine) as db:
        from app.application.gap_detector.gap_service import GapDetectorService
        import asyncio

        service = GapDetectorService(db)
        # Run async in sync context
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(service.analyze_skill_gaps(UUID(skill_id)))
        loop.close()

    return {
        "skill_id": skill_id,
        "misconceptions_found": len(results),
        "details": results,
    }


@celery_app.task(bind=True, name="gap_analysis.periodic_scan")
def periodic_gap_scan_task(self):
    """
    Periodic task to scan all skills for misconceptions.
    Should be scheduled via Celery Beat.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.core.config import get_settings

    settings = get_settings()
    engine = create_engine(settings.SYNC_DATABASE_URL)

    with Session(engine) as db:
        from app.infrastructure.db.models.content import SkillModel
        skills = db.query(SkillModel).all()

        results = []
        for skill in skills:
            task = analyze_skill_gaps_task.delay(str(skill.id))
            results.append({"skill_id": str(skill.id), "task_id": task.id})

    return {"tasks_dispatched": len(results)}
