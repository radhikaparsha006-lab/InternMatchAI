"""
Test Closed-Loop Feedback Flow:
Demonstrating that completing roadmap items updates student profile competencies,
recalculates the Internship Readiness Index (IRI), and updates recommendations.
"""

import pytest
import pytest_asyncio
from backend.database.connection import init_db, AsyncSessionLocal
from backend.database.repository import DataRepository
from backend.domain.closed_loop import ClosedLoopCoordinator
from backend.domain.readiness import ReadinessEngine
from backend.database.seed_data import SEED_INTERNSHIPS, DEMO_STUDENT

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()
    async with AsyncSessionLocal() as session:
        repo = DataRepository(session)
        await repo.seed_initial_data_if_needed()
    yield

@pytest.mark.asyncio
async def test_closed_loop_roadmap_completion_flow():
    async with AsyncSessionLocal() as session:
        repo = DataRepository(session)
        coordinator = ClosedLoopCoordinator(repo)

        student_id = DEMO_STUDENT["id"]
        target_internship_id = "intern_01"  # CloudScale Backend Intern
        internship = next(i for i in SEED_INTERNSHIPS if i["id"] == target_internship_id)

        # Baseline readiness before learning FastAPI
        skills_before = await repo.get_student_skills(student_id)
        profile_before = await repo.get_student_profile(student_id)
        projects_before = await repo.get_student_projects(student_id)

        student_data_before = {
            "profile": {
                "headline": profile_before.headline,
                "bio": profile_before.bio,
                "education_degree": profile_before.education_degree,
                "education_major": profile_before.education_major,
                "graduation_year": profile_before.graduation_year,
                "gpa": float(profile_before.gpa) if profile_before.gpa else None,
                "preferred_roles": profile_before.preferred_roles or []
            },
            "skills": skills_before,
            "projects": [{"title": p.title, "technologies": p.technologies} for p in projects_before]
        }
        baseline_iri = ReadinessEngine.calculate_iri(student_data_before, internship, roadmap_progress=0.0)

        # Student completes roadmap item for "FastAPI"
        update_result = await coordinator.handle_roadmap_item_completed(
            student_id=student_id,
            target_internship_id=target_internship_id,
            skill_name="FastAPI"
        )

        assert update_result["action"] == "roadmap_completed"
        assert update_result["provenance"] == "learning_progress"

        # Check student skills now has FastAPI
        skills_after = await repo.get_student_skills(student_id)
        skill_names_after = [s["canonical_name"] for s in skills_after]
        assert "FastAPI" in skill_names_after

        # Verify that provenance was preserved as learning_progress
        fastapi_skill = next(s for s in skills_after if s["canonical_name"] == "FastAPI")
        assert fastapi_skill["provenance"] == "learning_progress"

        # Check new IRI is higher than baseline
        assert update_result["new_iri"] > baseline_iri["overall_iri"]
