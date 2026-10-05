"""
Internship Readiness Index (IRI) Router.
Calculates and audits the composite readiness index for a given student and target role.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.database.models import ReadinessRecordModel
from backend.schemas.api_schemas import ReadinessResponse, ReadinessComponents
from backend.domain.readiness import ReadinessEngine
from datetime import datetime

router = APIRouter(prefix="", tags=["Readiness Index"])

@router.get("/readiness/{student_id}/{internship_id}", response_model=ReadinessResponse)
async def get_readiness_index(
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

    profile = await repo.get_student_profile(student_id)
    skills = await repo.get_student_skills(student_id)
    projects = await repo.get_student_projects(student_id)
    roadmap = await repo.get_roadmap(student_id, internship_id)

    # Check if student completed an interview session or answered questions for this internship
    from sqlalchemy import select, desc
    from backend.database.models import InterviewSessionModel, InterviewExchangeModel
    sess_stmt = (
        select(InterviewSessionModel)
        .where(
            InterviewSessionModel.student_id == student_id,
            InterviewSessionModel.target_internship_id == internship_id
        )
        .order_by(desc(InterviewSessionModel.created_at))
        .limit(1)
    )
    sess_res = await db.execute(sess_stmt)
    latest_session = sess_res.scalar_one_or_none()
    interview_score = None
    if latest_session:
        if latest_session.status == "completed" and latest_session.overall_score:
            interview_score = float(latest_session.overall_score)
        else:
            ex_stmt = select(InterviewExchangeModel).where(
                InterviewExchangeModel.session_id == latest_session.id,
                InterviewExchangeModel.correctness_score.isnot(None)
            )
            ex_res = await db.execute(ex_stmt)
            answered = ex_res.scalars().all()
            if answered:
                scores = [
                    float(e.correctness_score or 0) * 0.45 +
                    float(e.technical_depth_score or 0) * 0.35 +
                    float(e.clarity_score or 0) * 0.20
                    for e in answered
                ]
                interview_score = round(sum(scores) / len(scores), 1)

    student_data = {
        "profile": {
            "headline": profile.headline if profile else "",
            "bio": profile.bio if profile else "",
            "education_degree": profile.education_degree if profile else "",
            "education_major": profile.education_major if profile else "",
            "graduation_year": profile.graduation_year if profile else None,
            "gpa": float(profile.gpa) if profile and profile.gpa else None,
            "preferred_roles": profile.preferred_roles if profile else []
        },
        "skills": skills,
        "projects": [{"title": p.title, "technologies": p.technologies} for p in projects]
    }

    internship_dict = {
        "id": internship.id,
        "title": internship.title,
        "role_category": internship.role_category,
        "required_skills": internship.required_skills,
        "preferred_skills": internship.preferred_skills
    }

    roadmap_progress = float(roadmap.overall_progress) if roadmap else 0.0

    readiness = ReadinessEngine.calculate_iri(
        student_data=student_data,
        internship=internship_dict,
        roadmap_progress=roadmap_progress,
        interview_score=interview_score
    )

    # Record in DB audit trail
    import uuid
    record = ReadinessRecordModel(
        id=f"iri_{uuid.uuid4().hex[:16]}",
        student_id=student_id,
        target_internship_id=internship_id,
        overall_iri=readiness["overall_iri"],
        skill_coverage_score=readiness["components"]["skill_coverage"],
        project_evidence_score=readiness["components"]["project_evidence"],
        roadmap_progress_score=readiness["components"]["roadmap_progress"],
        interview_performance_score=readiness["components"]["interview_performance"],
        profile_completeness_score=readiness["components"]["profile_completeness"],
        explanation=readiness["explanation"],
        recorded_at=datetime.utcnow()
    )
    db.add(record)
    await db.commit()

    return ReadinessResponse(
        target_internship_id=internship_id,
        overall_iri=readiness["overall_iri"],
        components=ReadinessComponents(**readiness["components"]),
        matched_required_skills=readiness["matched_required_skills"],
        missing_required_skills=readiness["missing_required_skills"],
        explanation=readiness["explanation"]
    )
