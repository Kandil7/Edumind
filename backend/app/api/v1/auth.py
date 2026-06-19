from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_access_token,
    get_current_user, UserRole,
)
from app.domain.entities.student import Student
from app.infrastructure.db.repositories import SQLStudentRepository
from app.api.schemas.content import UserRegister, UserLogin, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(body: UserRegister, db: AsyncSession = Depends(get_db)):
    repo = SQLStudentRepository(db)
    existing = await repo.get_by_email(body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(
        id=uuid4(),
        name=body.name,
        email=body.email,
        preferred_language=body.preferred_language,
    )
    created = await repo.create(student)

    token = create_access_token({
        "sub": str(created.id),
        "email": created.email,
        "role": body.role,
        "user_id": str(created.id),
    })
    return TokenResponse(
        access_token=token,
        role=body.role,
        user_id=str(created.id),
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin, db: AsyncSession = Depends(get_db)):
    repo = SQLStudentRepository(db)
    student = await repo.get_by_email(body.email)
    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(student.id),
        "email": student.email,
        "role": "student",
        "user_id": str(student.id),
    })
    return TokenResponse(
        access_token=token,
        role="student",
        user_id=str(student.id),
    )


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {
        "user_id": user.get("user_id"),
        "email": user.get("email"),
        "role": user.get("role"),
    }
