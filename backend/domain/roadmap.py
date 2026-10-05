"""
Personalized Preparation Roadmap & Learning Resource Engine.
Sequences missing competencies respecting prerequisite dependencies,
attaches trusted learning resources with valid documentation URLs,
and recommends role-specific portfolio projects.
"""

from typing import Dict, Any, List, Set
from backend.domain.taxonomy import get_skill_metadata, SKILL_TAXONOMY
from backend.database.seed_data import TRUSTED_LEARNING_RESOURCES, CURATED_PORTFOLIO_PROJECTS

class RoadmapGenerator:
    @staticmethod
    def _sort_by_prerequisites(skills_to_learn: List[str]) -> List[str]:
        """
        Topologically sorts skills so foundational skills precede dependent frameworks.
        e.g., Python before FastAPI, SQL before PostgreSQL, JavaScript before React/Node.
        """
        ordered: List[str] = []
        visited: Set[str] = set()

        def visit(skill: str):
            if skill in visited:
                return
            meta = get_skill_metadata(skill) or {}
            prereqs = meta.get("prerequisites", [])
            for p in prereqs:
                if p in skills_to_learn and p not in visited:
                    visit(p)
            visited.add(skill)
            ordered.append(skill)

        for s in skills_to_learn:
            visit(s)

        return ordered

    @staticmethod
    def generate_roadmap(
        student_id: str,
        internship: Dict[str, Any],
        gap_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Constructs a complete personalized preparation roadmap.
        """
        critical_skills = [g["skill_name"] for g in gap_analysis["gaps"]["critical"]]
        important_skills = [g["skill_name"] for g in gap_analysis["gaps"]["important"]]
        useful_skills = [g["skill_name"] for g in gap_analysis["gaps"]["useful"]]

        # Sort each priority tier by prerequisite order
        ordered_critical = RoadmapGenerator._sort_by_prerequisites(critical_skills)
        ordered_important = RoadmapGenerator._sort_by_prerequisites(important_skills)
        ordered_useful = RoadmapGenerator._sort_by_prerequisites(useful_skills)

        items = []
        item_counter = 1

        # 1. Critical Milestones
        for skill in ordered_critical:
            meta = get_skill_metadata(skill) or {}
            resources = TRUSTED_LEARNING_RESOURCES.get(skill, [
                {
                    "title": f"{skill} Official Getting Started Guide",
                    "url": f"https://devdocs.io/{skill.lower().replace('.', '').replace(' ', '-')}/",
                    "platform": "Developer Documentation",
                    "type": "Documentation",
                    "estimated_hours": "6"
                }
            ])
            items.append({
                "id": f"item_{item_counter}",
                "skill_name": skill,
                "priority": "critical",
                "title": f"Master Core {skill} Competencies",
                "learning_objectives": f"Understand core principles of {skill}, build hands-on code examples, and practice implementing patterns expected in {internship.get('role_category')} roles.",
                "trusted_resources": resources,
                "practice_exercise": f"Build a focused proof-of-concept module demonstrating {skill} best practices.",
                "estimated_hours": int(resources[0].get("estimated_hours", 6)),
                "is_completed": False
            })
            item_counter += 1

        # 2. Important Milestones
        for skill in ordered_important:
            meta = get_skill_metadata(skill) or {}
            resources = TRUSTED_LEARNING_RESOURCES.get(skill, [
                {
                    "title": f"Introduction to {skill}",
                    "url": f"https://devdocs.io/{skill.lower().replace('.', '').replace(' ', '-')}/",
                    "platform": "Developer Documentation",
                    "type": "Tutorial",
                    "estimated_hours": "4"
                }
            ])
            items.append({
                "id": f"item_{item_counter}",
                "skill_name": skill,
                "priority": "important",
                "title": f"Strengthen Preferred Skill: {skill}",
                "learning_objectives": f"Learn practical usage of {skill} to distinguish your application during the interview stage.",
                "trusted_resources": resources,
                "practice_exercise": f"Integrate {skill} into your existing development workflow or project repository.",
                "estimated_hours": int(resources[0].get("estimated_hours", 4)),
                "is_completed": False
            })
            item_counter += 1

        # 3. Useful Milestones
        for skill in ordered_useful[:2]:
            resources = TRUSTED_LEARNING_RESOURCES.get(skill, [
                {
                    "title": f"{skill} Fundamentals",
                    "url": "https://devdocs.io/",
                    "platform": "Developer Documentation",
                    "type": "Reference",
                    "estimated_hours": "3"
                }
            ])
            items.append({
                "id": f"item_{item_counter}",
                "skill_name": skill,
                "priority": "useful",
                "title": f"Explore Tooling: {skill}",
                "learning_objectives": f"Familiarize yourself with {skill} workflows and team conventions.",
                "trusted_resources": resources,
                "practice_exercise": f"Complete a basic configuration or command-line walkthrough for {skill}.",
                "estimated_hours": int(resources[0].get("estimated_hours", 3)),
                "is_completed": False
            })
            item_counter += 1

        # Recommended portfolio project
        role_category = internship.get("role_category", "Backend")
        project_rec = CURATED_PORTFOLIO_PROJECTS.get(
            role_category, 
            CURATED_PORTFOLIO_PROJECTS["Backend"]
        )

        total_hours = sum(i["estimated_hours"] for i in items)

        return {
            "student_id": student_id,
            "target_internship_id": internship.get("id"),
            "internship_title": internship.get("title"),
            "company": internship.get("company"),
            "role_category": role_category,
            "total_estimated_hours": total_hours,
            "overall_progress": 0.0,
            "items": items,
            "recommended_project": project_rec
        }
