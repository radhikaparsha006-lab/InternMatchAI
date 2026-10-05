"""
Closed-Loop Feedback Coordinator.
Bridges preparation milestones and interview outcomes back into the student's profile,
updating competencies, recalculating readiness, and refreshing recommendations.
"""

from typing import Dict, Any, Optional
from backend.database.repository import DataRepository
from backend.domain.readiness import ReadinessEngine
from backend.domain.skill_normalizer import SkillNormalizer

class ClosedLoopCoordinator:
    def __init__(self, repo: DataRepository):
        self.repo = repo

    async def handle_roadmap_item_completed(
        self,
        student_id: str,
        target_internship_id: str,
        skill_name: Optional[str]
    ) -> Dict[str, Any]:
        """
        Triggered when a student completes a preparation roadmap item.
        1. Upgrades/adds the skill to student's profile with 'learning_progress' provenance.
        2. Recalculates the student's IRI for this target internship.
        3. Returns the update summary.
        """
        if skill_name:
            canonical = SkillNormalizer.normalize(skill_name)
            await self.repo.upsert_student_skill(
                student_id=student_id,
                canonical_name=canonical,
                proficiency_level="intermediate",
                provenance="learning_progress"
            )

        # Fetch updated student data & internship
        student = await self.repo.get_student(student_id)
        profile = await self.repo.get_student_profile(student_id)
        skills = await self.repo.get_student_skills(student_id)
        projects = await self.repo.get_student_projects(student_id)
        internship = await self.repo.get_internship_by_id(target_internship_id)
        roadmap = await self.repo.get_roadmap(student_id, target_internship_id)

        student_data = {
            "profile": {
                "headline": profile.headline if profile else "",
                "bio": profile.bio if profile else "",
                "education_degree": profile.education_degree if profile else "",
                "education_major": profile.education_major if profile else "",
                "graduation_year": profile.graduation_year if profile else None,
                "gpa": float(profile.gpa) if profile and profile.gpa else None,
                "preferred_roles": profile.preferred_roles if profile else []
            },
            "skills": skills,
            "projects": [{"title": p.title, "technologies": p.technologies} for p in projects]
        }

        progress = float(roadmap.overall_progress) if roadmap else 0.0
        new_iri_data = ReadinessEngine.calculate_iri(
            student_data=student_data,
            internship={
                "id": internship.id,
                "title": internship.title,
                "role_category": internship.role_category,
                "required_skills": internship.required_skills,
                "preferred_skills": internship.preferred_skills
            },
            roadmap_progress=progress
        )

        return {
            "action": "roadmap_completed",
            "updated_skill": skill_name,
            "provenance": "learning_progress",
            "new_iri": new_iri_data["overall_iri"],
            "explanation": new_iri_data["explanation"]
        }

    async def handle_interview_performance_verified(
        self,
        student_id: str,
        target_internship_id: str,
        tested_skill: Optional[str],
        score: float
    ) -> Dict[str, Any]:
        """
        Triggered when a student successfully answers a mock interview question.
        If score >= 70, registers the skill as 'interview_verified'.
        """
        if tested_skill and score >= 70.0:
            canonical = SkillNormalizer.normalize(tested_skill)
            await self.repo.upsert_student_skill(
                student_id=student_id,
                canonical_name=canonical,
                proficiency_level="advanced" if score >= 85.0 else "intermediate",
                provenance="interview_verified"
            )

        return {
            "action": "interview_verified",
            "tested_skill": tested_skill,
            "score": score,
            "provenance": "interview_verified" if score >= 70.0 else "unverified"
        }
