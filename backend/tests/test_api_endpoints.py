"""
Integration tests for FastAPI REST Endpoints.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database.connection import init_db, AsyncSessionLocal
from backend.database.repository import DataRepository

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_test_db():
    await init_db()
    async with AsyncSessionLocal() as session:
        repo = DataRepository(session)
        await repo.seed_initial_data_if_needed()
    yield

@pytest.mark.asyncio
async def test_health_check_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "InternMatch AI"

@pytest.mark.asyncio
async def test_student_profile_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get demo student profile
        res = await client.get("/api/profile/student_demo_01")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == "student_demo_01"
        assert bool(data["full_name"])
        assert len(data["skills"]) >= 4

        # Add a new skill
        add_res = await client.post(
            "/api/profile/student_demo_01/skills",
            json={"skill_name": "Docker", "proficiency_level": "intermediate"}
        )
        assert add_res.status_code == 200
        assert "Docker" in add_res.json()["message"]

@pytest.mark.asyncio
async def test_update_student_name_persistence():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Update name to "Rahul Kumar"
        update_res = await client.put(
            "/api/profile/student_demo_01",
            json={
                "full_name": "Rahul Kumar",
                "headline": "Full-Stack Engineer & AI Enthusiast"
            }
        )
        assert update_res.status_code == 200
        assert update_res.json()["full_name"] == "Rahul Kumar"

        # 2. Verify GET /profile returns "Rahul Kumar"
        get_res = await client.get("/api/profile/student_demo_01")
        assert get_res.status_code == 200
        assert get_res.json()["full_name"] == "Rahul Kumar"

        # 3. Verify Dashboard endpoint reflects "Rahul Kumar"
        dash_res = await client.get("/api/dashboard/student_demo_01")
        assert dash_res.status_code == 200
        assert dash_res.json()["student"]["full_name"] == "Rahul Kumar"

        # 4. Clean up / revert back
        revert_res = await client.put(
            "/api/profile/student_demo_01",
            json={"full_name": "Alex Chen", "headline": "Aspiring Backend & Machine Learning Engineer"}
        )
        assert revert_res.status_code == 200
        assert revert_res.json()["full_name"] == "Alex Chen"

@pytest.mark.asyncio
async def test_resume_parser_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resume_text = """
        Jordan Lee
        Enrolled in BS Computer Science, graduating in 2026. GPA: 3.82.
        Passionate about Python, FastAPI, and PostgreSQL database development.
        Built REST APIs with automated testing in Pytest and Docker.
        """
        res = await client.post("/api/resume/parse", json={"resume_text": resume_text})
        assert res.status_code == 200
        data = res.json()
        assert data["graduation_year"] == 2026
        skill_names = [s["skill_name"] for s in data["skills"]]
        assert "Python" in skill_names
        assert "FastAPI" in skill_names

@pytest.mark.asyncio
async def test_internships_and_recommendations():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # List internships
        list_res = await client.get("/api/internships")
        assert list_res.status_code == 200
        internships = list_res.json()
        assert len(internships) >= 10

        # Hybrid recommendations
        rec_res = await client.get("/api/recommendations/student_demo_01?model=hybrid")
        assert rec_res.status_code == 200
        rec_data = rec_res.json()
        assert rec_data["model_used"] == "hybrid_ranker"
        assert len(rec_data["items"]) > 0
        top = rec_data["items"][0]
        assert "match_score" in top
        assert "breakdown" in top
        assert "explanation" in top

@pytest.mark.asyncio
async def test_skill_gap_and_roadmap_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Skill gap
        gap_res = await client.get("/api/skill-gap/student_demo_01/intern_01")
        assert gap_res.status_code == 200
        gap_data = gap_res.json()
        assert gap_data["target_internship_id"] == "intern_01"
        assert "critical" in gap_data["gaps"]

        # Roadmap
        road_res = await client.get("/api/roadmap/student_demo_01/intern_01")
        assert road_res.status_code == 200
        road_data = road_res.json()
        assert len(road_data["items"]) > 0

        # Toggle roadmap item
        first_item = road_data["items"][0]
        toggle_res = await client.post(
            f"/api/roadmap/student_demo_01/intern_01/item/{first_item['id']}/toggle",
            json={"is_completed": True}
        )
        assert toggle_res.status_code == 200
        toggle_data = toggle_res.json()
        assert toggle_data["is_completed"] is True
        assert toggle_data["overall_progress"] > 0

@pytest.mark.asyncio
async def test_readiness_and_dashboard_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Readiness
        iri_res = await client.get("/api/readiness/student_demo_01/intern_01")
        assert iri_res.status_code == 200
        iri_data = iri_res.json()
        assert 0.0 <= iri_data["overall_iri"] <= 100.0

        # Dashboard summary
        dash_res = await client.get("/api/dashboard/student_demo_01")
        assert dash_res.status_code == 200
        dash_data = dash_res.json()
        assert "student" in dash_data
        assert "top_match" in dash_data
        assert "applications_pipeline" in dash_data
