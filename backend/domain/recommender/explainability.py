"""
Explainability Engine.
Decomposes recommendation scores into verifiable factor attributions and
generates evidence-grounded natural explanations.
"""

from typing import Dict, Any, List

class RecommendationExplainer:
    @staticmethod
    def generate_explanation(
        breakdown: Dict[str, float],
        matched_required: List[str],
        matched_preferred: List[str],
        missing_required: List[str],
        matching_projects: List[str],
        role_category: str
    ) -> str:
        """
        Synthesizes a grounded explanation from exact evidence.
        """
        parts = []

        # Skills attribution
        if matched_required:
            skills_str = ", ".join(matched_required[:3])
            parts.append(f"Strong competency alignment: your {skills_str} skills directly match the core requirements for this {role_category} role.")
        elif matched_preferred:
            skills_str = ", ".join(matched_preferred[:2])
            parts.append(f"Partial match: your {skills_str} skills meet several preferred qualifications for this role.")
        else:
            parts.append(f"You have foundational interest in {role_category}, though key required technologies remain to be demonstrated.")

        # Project attribution
        if matching_projects:
            proj_str = ", ".join(matching_projects[:2])
            parts.append(f"Your project work ({proj_str}) demonstrates practical application in this domain.")

        # Education & Preferences attribution
        if breakdown.get("education_score", 0) >= 80:
            parts.append("Your degree program and academic background fit the educational criteria.")

        # Key Gap attribution
        if missing_required:
            gaps_str = ", ".join(missing_required[:2])
            parts.append(f"Highest-priority growth areas to focus on: {gaps_str}.")

        return " ".join(parts)
