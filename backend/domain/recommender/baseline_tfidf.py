"""
Baseline Recommendation Engine: TF-IDF + Cosine Similarity.
Provides a transparent, benchmark baseline for comparing advanced models.
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BaselineTFIDFRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=2500
        )

    def _build_student_corpus(self, student_data: Dict[str, Any]) -> str:
        """Converts structured student profile and competencies into a single document."""
        profile = student_data.get("profile") or {}
        skills = student_data.get("skills") or []
        projects = student_data.get("projects") or []

        skill_names = " ".join([s.get("canonical_name") or s.get("skill_name") or "" for s in skills])
        project_texts = " ".join([
            f"{p.get('title', '')} {p.get('description', '')} {' '.join(p.get('technologies', []))}"
            for p in projects
        ])
        preferred_roles = " ".join(profile.get("preferred_roles") or [])

        corpus = (
            f"{profile.get('headline', '')} "
            f"{profile.get('education_degree', '')} {profile.get('education_major', '')} "
            f"{profile.get('bio', '')} "
            f"{preferred_roles} "
            f"{skill_names} {skill_names} "  # Boost skill weights
            f"{project_texts}"
        )
        return corpus.strip()

    def _build_internship_corpus(self, internship: Dict[str, Any]) -> str:
        """Converts internship requirements into a single document."""
        req_skills = " ".join(internship.get("required_skills") or [])
        pref_skills = " ".join(internship.get("preferred_skills") or [])
        
        corpus = (
            f"{internship.get('title', '')} "
            f"{internship.get('role_category', '')} "
            f"{internship.get('description', '')} "
            f"{internship.get('education_requirement', '')} "
            f"{req_skills} {req_skills} "  # Boost required skills
            f"{pref_skills}"
        )
        return corpus.strip()

    def compute_scores(
        self, 
        student_data: Dict[str, Any], 
        internships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Computes cosine similarity between student representation and each internship.
        Returns a list of dicts with internship_id, baseline_score (0-100), and rank.
        """
        if not internships:
            return []

        student_text = self._build_student_corpus(student_data)
        internship_texts = [self._build_internship_corpus(i) for i in internships]

        all_docs = [student_text] + internship_texts
        tfidf_matrix = self.vectorizer.fit_transform(all_docs)

        student_vector = tfidf_matrix[0:1]
        internship_vectors = tfidf_matrix[1:]

        similarities = cosine_similarity(student_vector, internship_vectors)[0]

        results = []
        for i, intern in enumerate(internships):
            sim = float(similarities[i])
            # Scale cosine similarity (0.0 - 1.0) to 0 - 100 with smooth min-max clamp
            score = round(float(np.clip(sim * 100, 0.0, 100.0)), 2)
            results.append({
                "internship_id": intern["id"],
                "score": score,
                "model": "baseline_tfidf"
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
