"""
Application Tracker Router.
Provides complete lifecycle tracking for internship applications
(saved, planning_to_apply, applied, assessment, interview, offer, rejected).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.schemas.api_schemas import ApplicationItem, UpsertApplicationRequest

router = APIRouter(prefix="", tags=["Applications"])

@router.get("/applications/{student_id}", response_model=List[ApplicationItem])
async def list_applications(student_id: str, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    apps = await repo.get_student_applications(student_id)
    return [
        ApplicationItem(
            id=a["id"],
            student_id=a["student_id"],
            internship_id=a["internship_id"],
            title=a["title"],
            company=a["company"],
            role_category=a["role_category"],
            location=a["location"],
            is_remote=a["is_remote"],
            status=a["status"],
            applied_at=a["applied_at"],
            deadline=a["deadline"],
            notes=a["notes"] or "",
            updated_at=a["updated_at"]
        )
        for a in apps
    ]

@router.post("/applications/{student_id}", response_model=Dict[str, str])
async def save_or_update_application(
    student_id: str,
    req: UpsertApplicationRequest,
    db: AsyncSession = Depends(get_db)
):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    internship = await repo.get_internship_by_id(req.internship_id)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    await repo.upsert_application(
        student_id=student_id,
        internship_id=req.internship_id,
        status=req.status,
        notes=req.notes
    )

    return {"message": f"Application status updated to '{req.status}'"}
