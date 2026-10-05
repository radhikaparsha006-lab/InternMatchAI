"""
Semantic Matcher Engine.
Computes dense semantic similarity between the student's profile representation
and internship opportunity descriptions.
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.domain.taxonomy import get_canonical_skill, get_skill_metadata

class SemanticMatcher:
    def __init__(self):
        # Character & word n-gram analyzer to capture morphological and semantic sub-tokens
        self.vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 3),
            sublinear_tf=True,
            min_df=1
        )

    def _enrich_text(self, text: str, skills: List[str]) -> str:
        """Enriches text with taxonomic descriptions and categories to provide semantic depth."""
        enriched = [text]
        for s in skills:
            canonical = get_canonical_skill(s)
            if canonical:
                meta = get_skill_metadata(canonical)
                if meta:
                    enriched.append(f"{canonical} is a {meta.get('category')} skill: {meta.get('description', '')}")
                    if meta.get("aliases"):
                        enriched.append(" ".join(meta["aliases"]))
        return " ".join(enriched)

    def compute_semantic_scores(
        self, 
        student_data: Dict[str, Any], 
        internships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Computes semantic similarity scores on a 0-100 scale."""
        if not internships:
            return []

        student_skills = [
            s.get("canonical_name") or s.get("skill_name") or "" 
            for s in (student_data.get("skills") or [])
        ]
        profile = student_data.get("profile") or {}
        student_base = f"{profile.get('headline', '')} {profile.get('bio', '')} {' '.join(profile.get('preferred_roles') or [])}"
        student_enriched = self._enrich_text(student_base, student_skills)

        internship_texts = []
        for i in internships:
            i_skills = (i.get("required_skills") or []) + (i.get("preferred_skills") or [])
            i_base = f"{i.get('title', '')} {i.get('role_category', '')} {i.get('description', '')} {i.get('education_requirement', '')}"
            i_enriched = self._enrich_text(i_base, i_skills)
            internship_texts.append(i_enriched)

        all_docs = [student_enriched] + internship_texts
        matrix = self.vectorizer.fit_transform(all_docs)

        student_vec = matrix[0:1]
        intern_vecs = matrix[1:]

        similarities = cosine_similarity(student_vec, intern_vecs)[0]

        results = []
        for i, intern in enumerate(internships):
            raw_sim = float(similarities[i])
            # Calibrate similarity curve smoothly
            calibrated = (raw_sim ** 0.8) * 100
            score = round(float(np.clip(calibrated, 0.0, 100.0)), 2)
            results.append({
                "internship_id": intern["id"],
                "score": score,
                "model": "semantic_dense"
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
