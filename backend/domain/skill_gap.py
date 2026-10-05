"""
Target-Specific Skill Gap Analysis.
Compares a student's demonstrated competencies against a specific target internship,
producing prioritized gaps: Critical (missing required), Important (missing preferred),
and Useful (supplementary/tools), along with overall competency coverage.
"""

from typing import Dict, Any, List, Set
from backend.domain.skill_normalizer import SkillNormalizer
from backend.domain.taxonomy import get_skill_metadata, SKILL_TAXONOMY

class SkillGapAnalyzer:
    @staticmethod
    def analyze_gaps(
        student_skills: List[Dict[str, Any]], 
        internship: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyzes and categorizes skill gaps between student competencies and target internship.
        """
        # Set of normalized student skill names
        possessed_skills: Set[str] = {
            SkillNormalizer.normalize(s.get("canonical_name") or s.get("skill_name") or "")
            for s in student_skills
        }
        possessed_skills.discard("")

        req_skills = [SkillNormalizer.normalize(s) for s in (internship.get("required_skills") or [])]
        pref_skills = [SkillNormalizer.normalize(s) for s in (internship.get("preferred_skills") or [])]

        # Categorize
        matched_required = [s for s in req_skills if s in possessed_skills]
        missing_required = [s for s in req_skills if s not in possessed_skills]

        matched_preferred = [s for s in pref_skills if s in possessed_skills]
        missing_preferred = [s for s in pref_skills if s not in possessed_skills]

        # Critical Gaps: missing required skills
        critical_gaps = []
        for s in missing_required:
            meta = get_skill_metadata(s) or {}
            critical_gaps.append({
                "skill_name": s,
                "category": meta.get("category", "General"),
                "priority": "critical",
                "reason": "Explicitly required for this internship role."
            })

        # Important Gaps: missing preferred skills
        important_gaps = []
        for s in missing_preferred:
            meta = get_skill_metadata(s) or {}
            important_gaps.append({
                "skill_name": s,
                "category": meta.get("category", "General"),
                "priority": "important",
                "reason": "Listed as a preferred/bonus qualification by the employer."
            })

        # Useful Gaps: complementary tools relevant to the role category
        role_category = internship.get("role_category", "")
        useful_gaps = []
        complementary_pool = {
            "Backend": ["Docker", "Redis", "Automated Testing", "CI/CD"],
            "Frontend": ["Tailwind CSS", "TypeScript", "Automated Testing"],
            "Full Stack": ["Docker", "Automated Testing", "CI/CD"],
            "Data Science": ["Git", "Communication", "Data Structures & Algorithms"],
            "Machine Learning": ["Docker", "Linux", "Scikit-Learn"]
        }.get(role_category, ["Git", "Communication"])

        for comp in complementary_pool:
            if comp not in possessed_skills and comp not in missing_required and comp not in missing_preferred:
                meta = get_skill_metadata(comp) or {}
                useful_gaps.append({
                    "skill_name": comp,
                    "category": meta.get("category", "Tools"),
                    "priority": "useful",
                    "reason": f"Valuable industry tool commonly expected in {role_category} teams."
                })

        # Calculate coverage ratio
        total_req = len(req_skills)
        coverage_ratio = round((len(matched_required) / total_req) * 100.0, 1) if total_req > 0 else 100.0

        # Severity
        if len(missing_required) == 0:
            severity = "Low (Readiness Ready)"
        elif len(missing_required) <= 2:
            severity = "Moderate (Achievable with targeted prep)"
        else:
            severity = "High (Significant preparation required)"

        return {
            "target_internship_id": internship.get("id"),
            "internship_title": internship.get("title"),
            "company": internship.get("company"),
            "role_category": role_category,
            "coverage_percentage": coverage_ratio,
            "severity": severity,
            "matched_skills": {
                "required": matched_required,
                "preferred": matched_preferred
            },
            "gaps": {
                "critical": critical_gaps,
                "important": important_gaps,
                "useful": useful_gaps[:3]  # Keep top 3 useful
            }
        }
