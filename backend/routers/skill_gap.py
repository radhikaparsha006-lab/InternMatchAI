"""
Skill Gap Analysis Router.
Computes prioritized competency gaps (Critical, Important, Useful)
for a selected target internship.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.schemas.api_schemas import SkillGapResponse, GapItem
from backend.domain.skill_gap import SkillGapAnalyzer

router = APIRouter(prefix="", tags=["Skill Gap"])

@router.get("/skill-gap/{student_id}/{internship_id}", response_model=SkillGapResponse)
async def get_skill_gap(
    student_id: str,
    internship_id: str,
    db: AsyncSession = Depends(get_db)
):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    internship = await repo.get_internship_by_id(internship_id)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    skills = await repo.get_student_skills(student_id)

    analysis = SkillGapAnalyzer.analyze_gaps(
        student_skills=skills,
        internship={
            "id": internship.id,
            "title": internship.title,
            "company": internship.company,
            "role_category": internship.role_category,
            "required_skills": internship.required_skills,
            "preferred_skills": internship.preferred_skills
        }
    )

    return SkillGapResponse(
        target_internship_id=internship.id,
        internship_title=internship.title,
        company=internship.company,
        role_category=internship.role_category,
        coverage_percentage=analysis["coverage_percentage"],
        severity=analysis["severity"],
        matched_skills=analysis["matched_skills"],
        gaps={
            "critical": [GapItem(**g) for g in analysis["gaps"]["critical"]],
            "important": [GapItem(**g) for g in analysis["gaps"]["important"]],
            "useful": [GapItem(**g) for g in analysis["gaps"]["useful"]]
        }
    )
