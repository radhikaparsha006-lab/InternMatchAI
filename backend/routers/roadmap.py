"""
Preparation Roadmap Router.
Generates prerequisite-ordered roadmaps, manages task progression,
and coordinates closed-loop skill updates upon milestone completion.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.database.models import RoadmapModel, RoadmapItemModel
from backend.schemas.api_schemas import (
    RoadmapResponse, RoadmapItemData, TrustedResource, RecommendedProject, ToggleRoadmapItemRequest
)
from backend.domain.skill_gap import SkillGapAnalyzer
from backend.domain.roadmap import RoadmapGenerator
from backend.domain.closed_loop import ClosedLoopCoordinator

router = APIRouter(prefix="", tags=["Roadmap"])

@router.get("/roadmap/{student_id}/{internship_id}", response_model=RoadmapResponse)
async def get_or_create_roadmap(
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

    # Check if existing roadmap in DB
    existing_roadmap = await repo.get_roadmap(student_id, internship_id)
    if existing_roadmap:
        items = await repo.get_roadmap_items(existing_roadmap.id)
        # Convert items to RoadmapItemData
        item_data_list = []
        for it in items:
            resources = [TrustedResource(**r) for r in (it.trusted_resources or [])]
            s_name = it.skill_name or it.title.replace("Master Core ", "").replace("Strengthen Preferred Skill: ", "").replace("Explore Tooling: ", "").replace(" Competencies", "").strip()
            item_data_list.append(RoadmapItemData(
                id=it.id,
                skill_name=s_name,
                priority=it.priority,
                title=it.title,
                learning_objectives=it.learning_objectives,
                trusted_resources=resources,
                practice_exercise=(it.practice_project or {}).get("description", "Complete milestone exercise."),
                estimated_hours=it.estimated_hours,
                is_completed=it.is_completed
            ))
        
        # Recommended project
        from backend.database.seed_data import CURATED_PORTFOLIO_PROJECTS
        rec_proj = CURATED_PORTFOLIO_PROJECTS.get(
            internship.role_category, 
            CURATED_PORTFOLIO_PROJECTS["Backend"]
        )

        return RoadmapResponse(
            student_id=student_id,
            target_internship_id=internship_id,
            internship_title=internship.title,
            company=internship.company,
            role_category=internship.role_category,
            total_estimated_hours=sum(it.estimated_hours for it in item_data_list),
            overall_progress=float(existing_roadmap.overall_progress),
            items=item_data_list,
            recommended_project=RecommendedProject(**rec_proj)
        )

    # Otherwise generate fresh roadmap
    skills = await repo.get_student_skills(student_id)
    internship_dict = {
        "id": internship.id,
        "title": internship.title,
        "company": internship.company,
        "role_category": internship.role_category,
        "required_skills": internship.required_skills,
        "preferred_skills": internship.preferred_skills
    }
    gap_analysis = SkillGapAnalyzer.analyze_gaps(skills, internship_dict)
    generated = RoadmapGenerator.generate_roadmap(student_id, internship_dict, gap_analysis)

    # Persist in DB
    roadmap_model = RoadmapModel(
        id=f"road_{student_id}_{internship_id}",
        student_id=student_id,
        target_internship_id=internship_id,
        overall_progress=0.0,
        status="active"
    )
    db.add(roadmap_model)
    await db.flush()

    saved_items = []
    for g_item in generated["items"]:
        item_model = RoadmapItemModel(
            id=f"{roadmap_model.id}_{g_item['id']}",
            roadmap_id=roadmap_model.id,
            skill_name=g_item["skill_name"],
            priority=g_item["priority"],
            title=g_item["title"],
            learning_objectives=g_item["learning_objectives"],
            trusted_resources=g_item["trusted_resources"],
            practice_project={"description": g_item["practice_exercise"]},
            estimated_hours=g_item["estimated_hours"],
            is_completed=False
        )
        db.add(item_model)
        saved_items.append(RoadmapItemData(
            id=item_model.id,
            skill_name=g_item["skill_name"],
            priority=g_item["priority"],
            title=g_item["title"],
            learning_objectives=g_item["learning_objectives"],
            trusted_resources=[TrustedResource(**r) for r in g_item["trusted_resources"]],
            practice_exercise=g_item["practice_exercise"],
            estimated_hours=g_item["estimated_hours"],
            is_completed=False
        ))

    await db.commit()

    return RoadmapResponse(
        student_id=student_id,
        target_internship_id=internship_id,
        internship_title=internship.title,
        company=internship.company,
        role_category=internship.role_category,
        total_estimated_hours=generated["total_estimated_hours"],
        overall_progress=0.0,
        items=saved_items,
        recommended_project=RecommendedProject(**generated["recommended_project"])
    )

@router.post("/roadmap/{student_id}/{internship_id}/item/{item_id}/toggle", response_model=Dict[str, Any])
async def toggle_roadmap_item(
    student_id: str,
    internship_id: str,
    item_id: str,
    req: ToggleRoadmapItemRequest,
    db: AsyncSession = Depends(get_db)
):
    repo = DataRepository(db)
    item = await repo.get_roadmap_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found")

    item.is_completed = req.is_completed
    item.completed_at = datetime.utcnow() if req.is_completed else None

    # Recalculate roadmap overall progress
    roadmap = await repo.get_roadmap(student_id, internship_id)
    if roadmap:
        all_items = await repo.get_roadmap_items(roadmap.id)
        completed_count = sum(1 for it in all_items if it.is_completed)
        total_count = len(all_items)
        new_progress = round((completed_count / total_count * 100.0), 1) if total_count > 0 else 0.0
        roadmap.overall_progress = new_progress

    await db.commit()

    # Closed-loop coordinator: if completed, register skill & update IRI
    closed_loop_result = None
    if req.is_completed:
        skill_name = item.skill_name or item.title.replace("Master Core ", "").replace("Strengthen Preferred Skill: ", "").replace("Explore Tooling: ", "").replace(" Competencies", "").strip()
        coordinator = ClosedLoopCoordinator(repo)
        closed_loop_result = await coordinator.handle_roadmap_item_completed(
            student_id=student_id,
            target_internship_id=internship_id,
            skill_name=skill_name
        )

    return {
        "item_id": item_id,
        "is_completed": item.is_completed,
        "overall_progress": float(roadmap.overall_progress) if roadmap else 0.0,
        "closed_loop_update": closed_loop_result
    }
