"""
Hybrid Recommendation Ranker.
Blends semantic similarity, required and preferred skill coverage,
project portfolio relevance, education compatibility, and student preferences.
"""

from typing import List, Dict, Any, Set
from backend.domain.skill_normalizer import SkillNormalizer
from backend.domain.recommender.semantic_matcher import SemanticMatcher
from backend.domain.recommender.explainability import RecommendationExplainer

class HybridRecommender:
    def __init__(
        self,
        w_req_skills: float = 0.35,
        w_semantic: float = 0.25,
        w_projects: float = 0.15,
        w_pref_skills: float = 0.10,
        w_education: float = 0.10,
        w_preferences: float = 0.05
    ):
        self.w_req = w_req_skills
        self.w_sem = w_semantic
        self.w_proj = w_projects
        self.w_pref = w_pref_skills
        self.w_edu = w_education
        self.w_prefs = w_preferences
        self.semantic_matcher = SemanticMatcher()

    def rank(
        self,
        student_data: Dict[str, Any],
        internships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculates hybrid ranking and explainable breakdown for each internship.
        """
        if not internships:
            return []

        # 1. Precompute semantic scores
        semantic_results = self.semantic_matcher.compute_semantic_scores(student_data, internships)
        semantic_map = {r["internship_id"]: r["score"] for r in semantic_results}

        # 2. Extract normalized student skills
        raw_skills = student_data.get("skills") or []
        student_skill_names = {
            SkillNormalizer.normalize(s.get("canonical_name") or s.get("skill_name") or "")
            for s in raw_skills
        }
        student_skill_names.discard("")

        # Student projects
        student_projects = student_data.get("projects") or []
        student_project_tech: Set[str] = set()
        for p in student_projects:
            for tech in (p.get("technologies") or []):
                norm = SkillNormalizer.normalize(tech)
                if norm:
                    student_project_tech.add(norm)

        # Profile info
        profile = student_data.get("profile") or {}
        student_roles = [r.lower() for r in (profile.get("preferred_roles") or [])]
        student_remote_pref = (profile.get("remote_preference") or "flexible").lower()

        ranked_items = []

        for intern in internships:
            i_id = intern["id"]
            req_skills = [SkillNormalizer.normalize(s) for s in (intern.get("required_skills") or [])]
            pref_skills = [SkillNormalizer.normalize(s) for s in (intern.get("preferred_skills") or [])]

            req_set = set(req_skills)
            pref_set = set(pref_skills)

            # A. Required Skill Score (0 - 100)
            matched_req = [s for s in req_skills if s in student_skill_names]
            missing_req = [s for s in req_skills if s not in student_skill_names]
            req_score = (len(matched_req) / len(req_skills) * 100.0) if req_skills else 100.0

            # B. Preferred Skill Score (0 - 100)
            matched_pref = [s for s in pref_skills if s in student_skill_names]
            pref_score = (len(matched_pref) / len(pref_skills) * 100.0) if pref_skills else 100.0

            # Combined Skills Score for reporting
            skills_score = round(0.75 * req_score + 0.25 * pref_score, 2)

            # C. Projects Relevance (0 - 100)
            matching_proj_titles = []
            overlap_count = 0
            for p in student_projects:
                p_techs = {SkillNormalizer.normalize(t) for t in (p.get("technologies") or [])}
                p_overlap = p_techs.intersection(req_set.union(pref_set))
                if p_overlap:
                    matching_proj_titles.append(p.get("title", "Project"))
                    overlap_count += len(p_overlap)

            if req_skills:
                proj_score = min(100.0, (overlap_count / max(1, len(req_skills))) * 100.0)
            else:
                proj_score = 75.0 if student_projects else 50.0
            proj_score = round(proj_score, 2)

            # D. Education Compatibility (0 - 100)
            edu_score = 85.0
            std_major = (profile.get("education_major") or "").lower()
            if any(term in std_major for term in ["computer", "software", "data", "engineering", "information"]):
                edu_score = 95.0
            edu_score = round(edu_score, 2)

            # E. Preferences Compatibility (0 - 100)
            pref_match_score = 70.0
            role_cat = intern.get("role_category", "").lower()
            if any(sr in role_cat or role_cat in sr for sr in student_roles):
                pref_match_score += 20.0
            if intern.get("is_remote") and student_remote_pref in ["remote_only", "flexible"]:
                pref_match_score += 10.0
            elif not intern.get("is_remote") and student_remote_pref in ["onsite_only", "flexible"]:
                pref_match_score += 10.0
            pref_match_score = round(min(100.0, pref_match_score), 2)

            # F. Semantic Score (0 - 100)
            sem_score = semantic_map.get(i_id, 50.0)

            # Composite Hybrid Score
            total_match_score = round(
                self.w_req * req_score +
                self.w_sem * sem_score +
                self.w_proj * proj_score +
                self.w_pref * pref_score +
                self.w_edu * edu_score +
                self.w_prefs * pref_match_score,
                2
            )

            breakdown = {
                "skills_score": skills_score,
                "projects_score": proj_score,
                "education_score": edu_score,
                "preferences_score": pref_match_score,
                "semantic_score": sem_score
            }

            explanation = RecommendationExplainer.generate_explanation(
                breakdown=breakdown,
                matched_required=matched_req,
                matched_preferred=matched_pref,
                missing_required=missing_req,
                matching_projects=matching_proj_titles,
                role_category=intern.get("role_category", "Engineering")
            )

            ranked_items.append({
                "internship_id": i_id,
                "match_score": total_match_score,
                "breakdown": breakdown,
                "explanation": explanation,
                "matched_required_skills": matched_req,
                "matched_preferred_skills": matched_pref,
                "missing_required_skills": missing_req,
                "internship": intern
            })

        ranked_items.sort(key=lambda x: x["match_score"], reverse=True)
        return ranked_items
