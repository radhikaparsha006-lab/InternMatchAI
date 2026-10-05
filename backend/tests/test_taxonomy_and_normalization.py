"""
Unit tests for Skill Taxonomy, Aliases, and Normalization.
"""

from backend.domain.taxonomy import get_canonical_skill, get_skill_metadata, get_all_canonical_skills
from backend.domain.skill_normalizer import SkillNormalizer

def test_alias_resolution():
    assert get_canonical_skill("python3") == "Python"
    assert get_canonical_skill("py") == "Python"
    assert get_canonical_skill("js") == "JavaScript"
    assert get_canonical_skill("react.js") == "React"
    assert get_canonical_skill("fastapi") == "FastAPI"
    assert get_canonical_skill("postgres") == "PostgreSQL"
    assert get_canonical_skill("dockerfile") == "Docker"
    assert get_canonical_skill("unknown_skill_xyz") is None

def test_skill_normalizer_list():
    raw_list = ["py", "Python", "fast-api", "docker", "unknown_tool"]
    normalized = SkillNormalizer.normalize_list(raw_list)
    assert "Python" in normalized
    assert "FastAPI" in normalized
    assert "Docker" in normalized
    # Duplicates like py and Python should be deduplicated
    assert normalized.count("Python") == 1

def test_extract_from_text():
    sample_text = """
    Experienced with Python and building REST APIs using FastAPI and PostgreSQL.
    Have written unit tests with Git version control and deployed with Docker containers.
    """
    extracted = SkillNormalizer.extract_from_text(sample_text)
    assert "Python" in extracted
    assert "FastAPI" in extracted
    assert "PostgreSQL" in extracted
    assert "REST APIs" in extracted
    assert "Docker" in extracted
    assert "Git" in extracted

def test_categorize_skills():
    skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Git", "Communication"]
    categorized = SkillNormalizer.categorize_skills(skills)
    assert "Python" in categorized.get("Languages", [])
    assert "FastAPI" in categorized.get("Frameworks", [])
    assert "PostgreSQL" in categorized.get("Databases", [])
    assert "Docker" in categorized.get("DevOps & Cloud", [])
    assert "Communication" in categorized.get("Soft Skills", [])
