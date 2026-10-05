"""
Unit tests for Recommender Engines: Baseline TF-IDF, Semantic Dense, Hybrid Ranker, and Explainability.
"""

from backend.domain.recommender.baseline_tfidf import BaselineTFIDFRecommender
from backend.domain.recommender.semantic_matcher import SemanticMatcher
from backend.domain.recommender.hybrid_ranker import HybridRecommender
from backend.domain.recommender.explainability import RecommendationExplainer
from backend.database.seed_data import SEED_INTERNSHIPS, DEMO_STUDENT

def test_baseline_tfidf_scoring():
    recommender = BaselineTFIDFRecommender()
    scores = recommender.compute_scores(DEMO_STUDENT, SEED_INTERNSHIPS)
    assert len(scores) == len(SEED_INTERNSHIPS)
    assert scores[0]["score"] >= scores[-1]["score"]
    # All scores should be bounded within [0, 100]
    for s in scores:
        assert 0.0 <= s["score"] <= 100.0
        assert s["model"] == "baseline_tfidf"

def test_semantic_matcher_scoring():
    matcher = SemanticMatcher()
    scores = matcher.compute_semantic_scores(DEMO_STUDENT, SEED_INTERNSHIPS)
    assert len(scores) == len(SEED_INTERNSHIPS)
    for s in scores:
        assert 0.0 <= s["score"] <= 100.0
        assert s["model"] == "semantic_dense"

def test_hybrid_recommender():
    hybrid = HybridRecommender()
    ranked = hybrid.rank(DEMO_STUDENT, SEED_INTERNSHIPS)
    assert len(ranked) == len(SEED_INTERNSHIPS)
    
    top = ranked[0]
    # Alex Chen is a backend-focused student with Python & SQL, so a Backend role should rank top
    assert top["internship"]["role_category"] in ["Backend", "Data Science", "Full Stack"]
    assert 0.0 <= top["match_score"] <= 100.0
    
    # Check breakdown schema
    breakdown = top["breakdown"]
    assert "skills_score" in breakdown
    assert "projects_score" in breakdown
    assert "education_score" in breakdown
    assert "preferences_score" in breakdown
    assert "semantic_score" in breakdown
    
    # Check explanation presence
    assert len(top["explanation"]) > 20
    assert "Python" in top["explanation"] or "SQL" in top["explanation"] or "competency" in top["explanation"].lower()

def test_explainability_grounding():
    explanation = RecommendationExplainer.generate_explanation(
        breakdown={"skills_score": 85.0, "education_score": 90.0},
        matched_required=["Python", "FastAPI"],
        matched_preferred=["Docker"],
        missing_required=["PostgreSQL"],
        matching_projects=["Course Enrollment API"],
        role_category="Backend"
    )
    assert "Python, FastAPI" in explanation
    assert "PostgreSQL" in explanation
    assert "Course Enrollment API" in explanation
