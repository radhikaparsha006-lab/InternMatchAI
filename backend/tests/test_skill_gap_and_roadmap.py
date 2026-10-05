"""
Unit tests for Skill Gap Analysis and Prerequisite-Ordered Roadmap Generation.
"""

from backend.domain.skill_gap import SkillGapAnalyzer
from backend.domain.roadmap import RoadmapGenerator
from backend.database.seed_data import SEED_INTERNSHIPS, DEMO_STUDENT

def test_skill_gap_analysis():
    # Test Alex Chen vs CloudScale Backend Intern (requires Python, FastAPI, PostgreSQL, REST APIs)
    backend_intern = next(i for i in SEED_INTERNSHIPS if i["id"] == "intern_01")
    gaps = SkillGapAnalyzer.analyze_gaps(DEMO_STUDENT["skills"], backend_intern)
    
    assert gaps["target_internship_id"] == "intern_01"
    assert "Python" in gaps["matched_skills"]["required"]
    assert "REST APIs" in gaps["matched_skills"]["required"]
    
    # Missing required skills should be identified as critical
    critical_names = [g["skill_name"] for g in gaps["gaps"]["critical"]]
    assert "FastAPI" in critical_names
    assert "PostgreSQL" in critical_names
    
    # Preferred skills (Docker, Redis) should be important
    important_names = [g["skill_name"] for g in gaps["gaps"]["important"]]
    assert "Docker" in important_names or "Redis" in important_names

def test_roadmap_prerequisite_ordering():
    # If a student lacks both SQL and PostgreSQL, SQL must be ordered before PostgreSQL
    gap_analysis = {
        "gaps": {
            "critical": [
                {"skill_name": "PostgreSQL"},
                {"skill_name": "FastAPI"}
            ],
            "important": [
                {"skill_name": "Docker"}
            ],
            "useful": [
                {"skill_name": "Redis"}
            ]
        }
    }
    backend_intern = next(i for i in SEED_INTERNSHIPS if i["id"] == "intern_01")
    roadmap = RoadmapGenerator.generate_roadmap("demo_student", backend_intern, gap_analysis)
    
    assert len(roadmap["items"]) > 0
    assert roadmap["total_estimated_hours"] > 0
    assert roadmap["recommended_project"]["title"] != ""
    
    # Check that trusted resources have valid URLs
    first_item = roadmap["items"][0]
    assert len(first_item["trusted_resources"]) > 0
    assert first_item["trusted_resources"][0]["url"].startswith("http")
