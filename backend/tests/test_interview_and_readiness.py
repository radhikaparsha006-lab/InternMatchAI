"""
Unit tests for Mock Interview Evaluation and Internship Readiness Index (IRI).
"""

from backend.domain.interview import MockInterviewEngine
from backend.domain.readiness import ReadinessEngine
from backend.database.seed_data import SEED_INTERNSHIPS, DEMO_STUDENT

def test_mock_interview_evaluation():
    engine = MockInterviewEngine()
    
    # Test a strong answer mentioning key concepts
    strong_answer = """
    FastAPI uses the Depends function for dependency injection. When working with database sessions,
    Depends yields the session per request and guarantees cleanup when the request completes.
    It provides modular architecture and makes writing automated tests easier.
    """
    eval_strong = engine.evaluate_response(
        question_text="Explain Depends in FastAPI",
        student_answer=strong_answer,
        tested_skill="FastAPI",
        ideal_keywords=["depends", "dependency injection", "yield", "database session", "cleanup"],
        model_highlights="Modular dependency injection",
        current_difficulty="medium"
    )
    
    assert eval_strong["overall_score"] >= 75.0
    assert eval_strong["correctness_score"] >= 70.0
    assert eval_strong["next_difficulty"] in ["medium", "hard"]
    
    # Test a weak / brief answer
    weak_answer = "I don't know much about it."
    eval_weak = engine.evaluate_response(
        question_text="Explain Depends in FastAPI",
        student_answer=weak_answer,
        tested_skill="FastAPI",
        ideal_keywords=["depends", "dependency injection"],
        model_highlights="Dependency injection",
        current_difficulty="medium"
    )
    assert eval_weak["overall_score"] <= 40.0
    assert eval_weak["next_difficulty"] == "easy"

def test_internship_readiness_index_calculation():
    backend_intern = next(i for i in SEED_INTERNSHIPS if i["id"] == "intern_01")
    
    # Initial state (0% roadmap, default interview score)
    initial_iri = ReadinessEngine.calculate_iri(
        student_data=DEMO_STUDENT,
        internship=backend_intern,
        roadmap_progress=0.0
    )
    assert 0.0 <= initial_iri["overall_iri"] <= 100.0
    
    # Advanced state (100% roadmap completed, high interview score)
    advanced_student = dict(DEMO_STUDENT)
    advanced_student["skills"] = DEMO_STUDENT["skills"] + [
        {"skill_name": "FastAPI", "proficiency_level": "intermediate"},
        {"skill_name": "PostgreSQL", "proficiency_level": "intermediate"}
    ]
    
    advanced_iri = ReadinessEngine.calculate_iri(
        student_data=advanced_student,
        internship=backend_intern,
        roadmap_progress=100.0,
        interview_score=90.0
    )
    
    # The advanced state MUST have a higher IRI than initial state
    assert advanced_iri["overall_iri"] > initial_iri["overall_iri"]
    assert advanced_iri["components"]["roadmap_progress"] == 100.0
    assert advanced_iri["components"]["interview_performance"] == 90.0
