"""
Internships & Recommendations Router.
Provides internship directory search and staged recommendation generation
(Baseline TF-IDF, Semantic Dense, and Hybrid Ranker).
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.schemas.api_schemas import (
    InternshipResponse, RecommendationListResponse, RecommendationItem, ScoreBreakdown
)
from backend.domain.recommender.baseline_tfidf import BaselineTFIDFRecommender
from backend.domain.recommender.semantic_matcher import SemanticMatcher
from backend.domain.recommender.hybrid_ranker import HybridRecommender

router = APIRouter(prefix="", tags=["Internships & Recommendations"])

@router.get("/internships", response_model=List[InternshipResponse])
async def list_internships(
    role: Optional[str] = Query(None, description="Filter by role category (e.g. Backend, Frontend)"),
    is_remote: Optional[bool] = Query(None, description="Filter remote positions"),
    search: Optional[str] = Query(None, description="Keyword search in title, company, skills"),
    db: AsyncSession = Depends(get_db)
):
    repo = DataRepository(db)
    internships = await repo.get_all_internships(role=role, is_remote=is_remote, query=search)
    return [
        InternshipResponse(
            id=i.id,
            title=i.title,
            company=i.company,
            role_category=i.role_category,
            location=i.location,
            is_remote=i.is_remote,
            duration_weeks=i.duration_weeks,
            stipend=i.stipend or "",
            description=i.description,
            education_requirement=i.education_requirement or "",
            required_skills=i.required_skills or [],
            preferred_skills=i.preferred_skills or [],
            application_deadline=i.application_deadline,
            source=i.source or "curated",
            source_url=i.source_url or ""
        )
        for i in internships
    ]

@router.get("/internships/{internship_id}", response_model=InternshipResponse)
async def get_internship_detail(internship_id: str, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    i = await repo.get_internship_by_id(internship_id)
    if not i:
        raise HTTPException(status_code=404, detail="Internship not found")
    return InternshipResponse(
        id=i.id,
        title=i.title,
        company=i.company,
        role_category=i.role_category,
        location=i.location,
        is_remote=i.is_remote,
        duration_weeks=i.duration_weeks,
        stipend=i.stipend or "",
        description=i.description,
        education_requirement=i.education_requirement or "",
        required_skills=i.required_skills or [],
        preferred_skills=i.preferred_skills or [],
        application_deadline=i.application_deadline,
        source=i.source or "curated",
        source_url=i.source_url or ""
    )

@router.get("/recommendations/{student_id}", response_model=RecommendationListResponse)
async def get_recommendations(
    student_id: str,
    model: str = Query("hybrid", description="Recommendation algorithm: 'hybrid', 'baseline_tfidf', 'semantic_dense'"),
    db: AsyncSession = Depends(get_db)
):
    repo = DataRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = await repo.get_student_profile(student_id)
    skills = await repo.get_student_skills(student_id)
    projects = await repo.get_student_projects(student_id)
    all_internships = await repo.get_all_internships()

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

    intern_by_id = {i["id"]: i for i in internship_dicts}

    if model == "baseline_tfidf":
        baseline = BaselineTFIDFRecommender()
        scores = baseline.compute_scores(student_data, internship_dicts)
        items = []
        for s in scores:
            intern = intern_by_id[s["internship_id"]]
            items.append(RecommendationItem(
                internship_id=intern["id"],
                match_score=s["score"],
                breakdown=ScoreBreakdown(
                    skills_score=s["score"],
                    projects_score=s["score"],
                    education_score=s["score"],
                    preferences_score=s["score"],
                    semantic_score=s["score"]
                ),
                explanation=f"Ranked by Baseline TF-IDF vector similarity over profile content and role description ({s['score']}/100).",
                matched_required_skills=[],
                matched_preferred_skills=[],
                missing_required_skills=intern.get("required_skills", []),
                internship=InternshipResponse(**intern)
            ))
        return RecommendationListResponse(
            model_used="baseline_tfidf",
            total_recommendations=len(items),
            items=items
        )

    elif model == "semantic_dense":
        semantic = SemanticMatcher()
        scores = semantic.compute_semantic_scores(student_data, internship_dicts)
        items = []
        for s in scores:
            intern = intern_by_id[s["internship_id"]]
            items.append(RecommendationItem(
                internship_id=intern["id"],
                match_score=s["score"],
                breakdown=ScoreBreakdown(
                    skills_score=s["score"],
                    projects_score=s["score"],
                    education_score=s["score"],
                    preferences_score=s["score"],
                    semantic_score=s["score"]
                ),
                explanation=f"Ranked by dense semantic representation similarity across domain competencies ({s['score']}/100).",
                matched_required_skills=[],
                matched_preferred_skills=[],
                missing_required_skills=intern.get("required_skills", []),
                internship=InternshipResponse(**intern)
            ))
        return RecommendationListResponse(
            model_used="semantic_dense",
            total_recommendations=len(items),
            items=items
        )

    else:  # Hybrid (Default)
        hybrid = HybridRecommender()
        ranked = hybrid.rank(student_data, internship_dicts)
        items = []
        for r in ranked:
            items.append(RecommendationItem(
                internship_id=r["internship_id"],
                match_score=r["match_score"],
                breakdown=ScoreBreakdown(**r["breakdown"]),
                explanation=r["explanation"],
                matched_required_skills=r["matched_required_skills"],
                matched_preferred_skills=r["matched_preferred_skills"],
                missing_required_skills=r["missing_required_skills"],
                internship=InternshipResponse(**r["internship"])
            ))
        return RecommendationListResponse(
            model_used="hybrid_ranker",
            total_recommendations=len(items),
            items=items
        )
