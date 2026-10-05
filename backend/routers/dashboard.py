"""
Student Dashboard Summary Router.
Aggregates top recommendations, active readiness index, applications pipeline,
and high-priority skill gaps into a unified student cockpit.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.domain.recommender.hybrid_ranker import HybridRecommender
from backend.domain.readiness import ReadinessEngine
from backend.domain.skill_gap import SkillGapAnalyzer

router = APIRouter(prefix="", tags=["Dashboard"])

@router.get("/dashboard/{student_id}", response_model=Dict[str, Any])
async def get_dashboard_summary(student_id: str, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = await repo.get_student_profile(student_id)
    skills = await repo.get_student_skills(student_id)
    projects = await repo.get_student_projects(student_id)
    all_internships = await repo.get_all_internships()
    applications = await repo.get_student_applications(student_id)

    student_data = {
        "profile": {
            "headline": profile.headline if profile else "",
            "bio": profile.bio if profile else "",
            "education_degree": profile.education_degree if profile else "",
            "education_major": profile.education_major if profile else "",
            "graduation_year": profile.graduation_year if profile else None,
            "gpa": float(profile.gpa) if profile and profile.gpa else None,
            "preferred_roles": profile.preferred_roles if profile else [],
            "remote_preference": profile.remote_preference if profile else "flexible"
        },
        "skills": skills,
        "projects": [{"title": p.title, "description": p.description, "technologies": p.technologies} for p in projects]
    }

    internship_dicts = [
        {
            "id": i.id,
            "title": i.title,
            "company": i.company,
            "role_category": i.role_category,
            "location": i.location,
            "is_remote": i.is_remote,
            "duration_weeks": i.duration_weeks,
            "stipend": i.stipend,
            "description": i.description,
            "education_requirement": i.education_requirement,
            "required_skills": i.required_skills,
            "preferred_skills": i.preferred_skills,
            "application_deadline": i.application_deadline,
            "source": i.source,
            "source_url": i.source_url
        }
        for i in all_internships
    ]

    # Compute top hybrid recommendations
    hybrid = HybridRecommender()
    ranked = hybrid.rank(student_data, internship_dicts)
    top_recommendations = ranked[:3] if ranked else []

    top_intern = top_recommendations[0]["internship"] if top_recommendations else None
    top_match_score = top_recommendations[0]["match_score"] if top_recommendations else 0.0

    # Calculate active readiness on the #1 target
    active_readiness = None
    if top_intern:
        roadmap = await repo.get_roadmap(student_id, top_intern["id"])
        progress = float(roadmap.overall_progress) if roadmap else 0.0
        active_readiness = ReadinessEngine.calculate_iri(
            student_data=student_data,
            internship=top_intern,
            roadmap_progress=progress
        )

    # Pipeline statistics
    app_stats = {
        "saved": sum(1 for a in applications if a["status"] == "saved"),
        "applied": sum(1 for a in applications if a["status"] in ["applied", "planning_to_apply"]),
        "interview": sum(1 for a in applications if a["status"] in ["assessment", "interview"]),
        "offers": sum(1 for a in applications if a["status"] == "offer"),
        "total": len(applications)
    }

    # High-priority gaps across top recommendation
    top_gaps = []
    if top_intern:
        gap_res = SkillGapAnalyzer.analyze_gaps(skills, top_intern)
        top_gaps = gap_res["gaps"]["critical"] + gap_res["gaps"]["important"][:1]

    return {
        "student": {
            "id": student.id,
            "full_name": student.full_name,
            "email": student.email,
            "headline": profile.headline if profile else "",
            "education": f"{profile.education_degree} in {profile.education_major}" if profile else "",
            "total_verified_skills": len(skills)
        },
        "top_match": {
            "internship_id": top_intern["id"] if top_intern else None,
            "title": top_intern["title"] if top_intern else "None",
            "company": top_intern["company"] if top_intern else "None",
            "match_score": top_match_score,
            "explanation": top_recommendations[0]["explanation"] if top_recommendations else ""
        },
        "active_readiness": active_readiness,
        "applications_pipeline": app_stats,
        "top_priority_gaps": top_gaps[:3],
        "recent_recommendations": [
            {
                "id": r["internship_id"],
                "title": r["internship"]["title"],
                "company": r["internship"]["company"],
                "role_category": r["internship"]["role_category"],
                "location": r["internship"]["location"],
                "is_remote": r["internship"]["is_remote"],
                "match_score": r["match_score"]
            }
            for r in top_recommendations
        ]
    }
