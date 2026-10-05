"""
Internship Readiness Index (IRI) Engine.
Computes an interpretable composite indicator (0-100 scale) of how prepared
a student currently is for a specific target internship.
"""

from typing import Dict, Any, List, Optional
from backend.domain.skill_normalizer import SkillNormalizer

class ReadinessEngine:
    W_SKILL = 0.35
    W_PROJECT = 0.20
    W_ROADMAP = 0.15
    W_INTERVIEW = 0.20
    W_PROFILE = 0.10

    @classmethod
    def calculate_iri(
        cls,
        student_data: Dict[str, Any],
        internship: Dict[str, Any],
        roadmap_progress: float = 0.0,
        interview_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates the Internship Readiness Index (0-100) with explainable components.
        """
        # 1. Skill Coverage Score (0 - 100)
        raw_skills = student_data.get("skills") or []
        student_skill_names = {
            SkillNormalizer.normalize(s.get("canonical_name") or s.get("skill_name") or "")
            for s in raw_skills
        }
        student_skill_names.discard("")

        req_skills = [SkillNormalizer.normalize(s) for s in (internship.get("required_skills") or [])]
        pref_skills = [SkillNormalizer.normalize(s) for s in (internship.get("preferred_skills") or [])]

        matched_req = [s for s in req_skills if s in student_skill_names]
        matched_pref = [s for s in pref_skills if s in student_skill_names]

        req_ratio = (len(matched_req) / len(req_skills)) if req_skills else 1.0
        pref_ratio = (len(matched_pref) / len(pref_skills)) if pref_skills else 1.0
        skill_coverage_score = round((0.75 * req_ratio + 0.25 * pref_ratio) * 100.0, 1)

        # 2. Project Evidence Score (0 - 100)
        projects = student_data.get("projects") or []
        proj_score = 0.0
        if projects:
            target_skills = set(req_skills + pref_skills)
            tech_matches = 0
            for p in projects:
                p_techs = {SkillNormalizer.normalize(t) for t in (p.get("technologies") or [])}
                if p_techs.intersection(target_skills):
                    tech_matches += 1
            proj_score = min(100.0, 50.0 + (tech_matches * 25.0))
        project_evidence_score = round(proj_score, 1)

        # 3. Roadmap Progress Score (0 - 100)
        roadmap_progress_score = round(float(min(100.0, max(0.0, roadmap_progress))), 1)

        # 4. Interview Performance Score (0 - 100)
        # Default baseline if untaken: 50.0
        actual_interview_score = round(float(interview_score), 1) if interview_score is not None else 50.0

        # 5. Profile Completeness Score (0 - 100)
        profile = student_data.get("profile") or {}
        comp_points = 0
        if profile.get("headline"): comp_points += 20
        if profile.get("bio"): comp_points += 20
        if profile.get("education_degree") and profile.get("education_major"): comp_points += 20
        if profile.get("gpa"): comp_points += 20
        if profile.get("preferred_roles"): comp_points += 20
        profile_completeness_score = float(comp_points)

        # Composite IRI
        overall_iri = round(
            cls.W_SKILL * skill_coverage_score +
            cls.W_PROJECT * project_evidence_score +
            cls.W_ROADMAP * roadmap_progress_score +
            cls.W_INTERVIEW * actual_interview_score +
            cls.W_PROFILE * profile_completeness_score,
            1
        )

        # Generate human-readable explanation
        components_summary = []
        if skill_coverage_score >= 70:
            components_summary.append("strong verified skill coverage")
        else:
            components_summary.append(f"moderate skill coverage ({len(matched_req)}/{len(req_skills)} required skills)")

        if roadmap_progress_score > 0:
            components_summary.append(f"{roadmap_progress_score}% roadmap completion")

        if interview_score is not None:
            components_summary.append(f"interview performance score of {actual_interview_score}/100")

        explanation = (
            f"Your current Internship Readiness Index is {overall_iri}/100. "
            f"This reflects {', '.join(components_summary)}, and portfolio project alignment. "
            f"Complete pending roadmap milestones and take mock interview practice to further elevate this score."
        )

        return {
            "overall_iri": overall_iri,
            "components": {
                "skill_coverage": skill_coverage_score,
                "project_evidence": project_evidence_score,
                "roadmap_progress": roadmap_progress_score,
                "interview_performance": actual_interview_score,
                "profile_completeness": profile_completeness_score
            },
            "matched_required_skills": matched_req,
            "missing_required_skills": [s for s in req_skills if s not in student_skill_names],
            "explanation": explanation
        }
