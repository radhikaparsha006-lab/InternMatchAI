"""
Profile & Resume Router.
Provides profile management, skill/project updates, and AI-assisted resume parsing.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.schemas.api_schemas import (
    StudentResponse, ProfileData, AddSkillRequest, ProjectItem,
    ResumeParseRequest, ResumeParseResponse
)
from backend.domain.skill_normalizer import SkillNormalizer
from backend.domain.resume_parser import ResumeParser

router = APIRouter(prefix="", tags=["Profile & Resume"])

@router.get("/profile/{student_id}", response_model=StudentResponse)
async def get_student_profile(student_id: str, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = await repo.get_student_profile(student_id)
    skills = await repo.get_student_skills(student_id)
    projects = await repo.get_student_projects(student_id)

    prof_data = None
    if profile:
        prof_data = ProfileData(
            headline=profile.headline or "",
            education_degree=profile.education_degree or "",
            education_major=profile.education_major or "",
            graduation_year=profile.graduation_year,
            gpa=float(profile.gpa) if profile.gpa is not None else None,
            bio=profile.bio or "",
            location=profile.location or "",
            remote_preference=profile.remote_preference or "flexible",
            preferred_roles=profile.preferred_roles or [],
            preferred_industries=profile.preferred_industries or []
        )

    return StudentResponse(
        id=student.id,
        email=student.email,
        full_name=student.full_name,
        profile=prof_data,
        skills=[
            {
                "id": s["id"],
                "canonical_name": s["canonical_name"],
                "category": s["category"],
                "proficiency_level": s["proficiency_level"],
                "provenance": s["provenance"]
            }
            for s in skills
        ],
        projects=[
            ProjectItem(
                id=p.id,
                title=p.title,
                description=p.description,
                technologies=p.technologies or [],
                github_url=p.github_url or "",
                live_url=p.live_url or ""
            )
            for p in projects
        ]
    )

@router.put("/profile/{student_id}", response_model=Dict[str, str])
async def update_profile(student_id: str, data: ProfileData, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    profile = await repo.get_student_profile(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile.headline = data.headline
    profile.education_degree = data.education_degree
    profile.education_major = data.education_major
    profile.graduation_year = data.graduation_year
    profile.gpa = data.gpa
    profile.bio = data.bio
    profile.location = data.location
    profile.remote_preference = data.remote_preference
    profile.preferred_roles = data.preferred_roles
    profile.preferred_industries = data.preferred_industries

    await db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/profile/{student_id}/skills", response_model=Dict[str, str])
async def add_student_skill(student_id: str, req: AddSkillRequest, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    canonical = SkillNormalizer.normalize(req.skill_name)
    if not canonical:
        raise HTTPException(status_code=400, detail="Invalid skill name")
    
    await repo.upsert_student_skill(
        student_id=student_id,
        canonical_name=canonical,
        proficiency_level=req.proficiency_level or "intermediate",
        provenance="user_provided"
    )
    return {"message": f"Skill '{canonical}' added successfully", "canonical_name": canonical}

@router.delete("/profile/{student_id}/skills/{skill_name}", response_model=Dict[str, str])
async def delete_student_skill(student_id: str, skill_name: str, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    canonical = SkillNormalizer.normalize(skill_name)
    success = await repo.remove_student_skill(student_id, canonical)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found on profile")
    return {"message": f"Skill '{canonical}' removed successfully"}

@router.post("/resume/parse", response_model=ResumeParseResponse)
async def parse_resume(req: ResumeParseRequest):
    """
    Parses resume text into a structured candidate profile for review and confirmation.
    """
    if not req.resume_text or len(req.resume_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Resume text must be at least 20 characters")

    parsed = ResumeParser.parse_text(req.resume_text)
    return ResumeParseResponse(**parsed)
