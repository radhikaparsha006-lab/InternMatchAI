"""
Repository Layer for Database Operations.
Provides high-level asynchronous data access for students, profiles,
skills, internships, roadmaps, interview sessions, readiness, and applications.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc
from backend.database.models import (
    StudentModel, StudentProfileModel, SkillModel, StudentSkillModel,
    StudentProjectModel, InternshipModel, RecommendationScoreModel,
    RoadmapModel, RoadmapItemModel, InterviewSessionModel,
    InterviewExchangeModel, ReadinessRecordModel, ApplicationModel
)
from backend.database.seed_data import (
    SEED_INTERNSHIPS, SKILL_TAXONOMY, DEMO_STUDENT
)

class DataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def seed_initial_data_if_needed(self) -> None:
        """Seeds canonical skills, internships, and demo student if tables are empty."""
        # 1. Seed Skills
        skill_res = await self.session.execute(select(SkillModel).limit(1))
        if not skill_res.scalar_one_or_none():
            skill_models = []
            for name, meta in SKILL_TAXONOMY.items():
                s = SkillModel(
                    id=f"skill_{name.lower().replace(' ', '_').replace('.', '_').replace('/', '_').replace('&', 'and').replace('+', 'plus').replace('-', '_').replace('(', '').replace(')', '')}",
                    canonical_name=name,
                    category=meta["category"],
                    aliases=meta["aliases"],
                    description=meta["description"]
                )
                skill_models.append(s)
            self.session.add_all(skill_models)
            await self.session.commit()

        # 2. Seed Internships
        intern_res = await self.session.execute(select(InternshipModel).limit(1))
        if not intern_res.scalar_one_or_none():
            intern_models = []
            for item in SEED_INTERNSHIPS:
                im = InternshipModel(
                    id=item["id"],
                    title=item["title"],
                    company=item["company"],
                    role_category=item["role_category"],
                    location=item["location"],
                    is_remote=item["is_remote"],
                    duration_weeks=item["duration_weeks"],
                    stipend=item["stipend"],
                    description=item["description"],
                    education_requirement=item["education_requirement"],
                    required_skills=item["required_skills"],
                    preferred_skills=item["preferred_skills"],
                    application_deadline=datetime.strptime(item["application_deadline"], "%Y-%m-%d").date(),
                    source=item["source"],
                    source_url=item["source_url"]
                )
                intern_models.append(im)
            self.session.add_all(intern_models)
            await self.session.commit()

        # 3. Seed Demo Student
        demo_id = DEMO_STUDENT["id"]
        stud_res = await self.session.execute(select(StudentModel).where(StudentModel.id == demo_id))
        if not stud_res.scalar_one_or_none():
            student = StudentModel(
                id=demo_id,
                email=DEMO_STUDENT["email"],
                full_name=DEMO_STUDENT["full_name"]
            )
            self.session.add(student)
            await self.session.flush()

            # Profile
            p = DEMO_STUDENT["profile"]
            profile = StudentProfileModel(
                id=f"prof_{demo_id}",
                student_id=demo_id,
                headline=p["headline"],
                education_degree=p["education_degree"],
                education_major=p["education_major"],
                graduation_year=p["graduation_year"],
                gpa=p["gpa"],
                bio=p["bio"],
                location=p["location"],
                remote_preference=p["remote_preference"],
                preferred_roles=p["preferred_roles"],
                preferred_industries=p["preferred_industries"]
            )
            self.session.add(profile)

            # Skills
            for sk in DEMO_STUDENT["skills"]:
                # Lookup skill id
                s_query = await self.session.execute(select(SkillModel).where(SkillModel.canonical_name == sk["skill_name"]))
                skill_obj = s_query.scalar_one_or_none()
                if skill_obj:
                    ss = StudentSkillModel(
                        id=f"ss_{demo_id}_{skill_obj.id}",
                        student_id=demo_id,
                        skill_id=skill_obj.id,
                        proficiency_level=sk["proficiency_level"],
                        provenance=sk["provenance"]
                    )
                    self.session.add(ss)

            # Projects
            for pr in DEMO_STUDENT["projects"]:
                sp = StudentProjectModel(
                    id=pr["id"],
                    student_id=demo_id,
                    title=pr["title"],
                    description=pr["description"],
                    technologies=pr["technologies"],
                    github_url=pr["github_url"],
                    live_url=pr["live_url"]
                )
                self.session.add(sp)

            await self.session.commit()

    # --- Student & Profile Operations ---
    async def get_student(self, student_id: str) -> Optional[StudentModel]:
        stmt = select(StudentModel).where(StudentModel.id == student_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_student_profile(self, student_id: str) -> Optional[StudentProfileModel]:
        stmt = select(StudentProfileModel).where(StudentProfileModel.student_id == student_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_student_skills(self, student_id: str) -> List[Dict[str, Any]]:
        stmt = (
            select(StudentSkillModel, SkillModel)
            .join(SkillModel, StudentSkillModel.skill_id == SkillModel.id)
            .where(StudentSkillModel.student_id == student_id)
        )
        res = await self.session.execute(stmt)
        results = []
        for ss, s in res.all():
            results.append({
                "id": ss.id,
                "skill_id": s.id,
                "canonical_name": s.canonical_name,
                "category": s.category,
                "proficiency_level": ss.proficiency_level,
                "provenance": ss.provenance,
                "verified_at": ss.verified_at
            })
        return results

    async def get_student_projects(self, student_id: str) -> List[StudentProjectModel]:
        stmt = select(StudentProjectModel).where(StudentProjectModel.student_id == student_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def upsert_student_skill(
        self, 
        student_id: str, 
        canonical_name: str, 
        proficiency_level: str = "intermediate", 
        provenance: str = "user_provided"
    ) -> None:
        """Upserts a student's skill record."""
        # Find or create skill
        s_res = await self.session.execute(select(SkillModel).where(SkillModel.canonical_name == canonical_name))
        skill = s_res.scalar_one_or_none()
        if not skill:
            skill = SkillModel(
                id=f"skill_{canonical_name.lower().replace(' ', '_')}",
                canonical_name=canonical_name,
                category="Other",
                aliases=[],
                description=f"Skill: {canonical_name}"
            )
            self.session.add(skill)
            await self.session.flush()

        # Check existing student skill
        ss_res = await self.session.execute(
            select(StudentSkillModel).where(
                StudentSkillModel.student_id == student_id,
                StudentSkillModel.skill_id == skill.id
            )
        )
        existing = ss_res.scalar_one_or_none()
        if existing:
            existing.proficiency_level = proficiency_level
            existing.provenance = provenance
            existing.verified_at = datetime.utcnow()
        else:
            new_ss = StudentSkillModel(
                id=f"ss_{student_id}_{skill.id}",
                student_id=student_id,
                skill_id=skill.id,
                proficiency_level=proficiency_level,
                provenance=provenance,
                verified_at=datetime.utcnow()
            )
            self.session.add(new_ss)
        await self.session.commit()

    async def remove_student_skill(self, student_id: str, canonical_name: str) -> bool:
        """Removes a skill from a student's profile."""
        s_res = await self.session.execute(select(SkillModel).where(SkillModel.canonical_name == canonical_name))
        skill = s_res.scalar_one_or_none()
        if not skill:
            return False
        stmt = delete(StudentSkillModel).where(
            StudentSkillModel.student_id == student_id,
            StudentSkillModel.skill_id == skill.id
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    # --- Internships Operations ---
    async def get_all_internships(
        self, 
        role: Optional[str] = None, 
        is_remote: Optional[bool] = None, 
        query: Optional[str] = None
    ) -> List[InternshipModel]:
        stmt = select(InternshipModel)
        if role and role.lower() != "all":
            stmt = stmt.where(InternshipModel.role_category.ilike(f"%{role}%"))
        if is_remote is not None:
            stmt = stmt.where(InternshipModel.is_remote == is_remote)
        
        res = await self.session.execute(stmt)
        internships = list(res.scalars().all())

        if query:
            q_lower = query.lower()
            internships = [
                i for i in internships
                if q_lower in i.title.lower() 
                or q_lower in i.company.lower() 
                or q_lower in i.description.lower()
                or any(q_lower in s.lower() for s in (i.required_skills or []))
            ]
        return internships

    async def get_internship_by_id(self, internship_id: str) -> Optional[InternshipModel]:
        stmt = select(InternshipModel).where(InternshipModel.id == internship_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # --- Roadmaps Operations ---
    async def get_roadmap(self, student_id: str, target_internship_id: str) -> Optional[RoadmapModel]:
        stmt = select(RoadmapModel).where(
            RoadmapModel.student_id == student_id,
            RoadmapModel.target_internship_id == target_internship_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_roadmap_items(self, roadmap_id: str) -> List[RoadmapItemModel]:
        stmt = select(RoadmapItemModel).where(RoadmapItemModel.roadmap_id == roadmap_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_roadmap_item_by_id(self, item_id: str) -> Optional[RoadmapItemModel]:
        stmt = select(RoadmapItemModel).where(RoadmapItemModel.id == item_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # --- Applications Operations ---
    async def get_student_applications(self, student_id: str) -> List[Dict[str, Any]]:
        stmt = (
            select(ApplicationModel, InternshipModel)
            .join(InternshipModel, ApplicationModel.internship_id == InternshipModel.id)
            .where(ApplicationModel.student_id == student_id)
            .order_by(desc(ApplicationModel.updated_at))
        )
        res = await self.session.execute(stmt)
        out = []
        for app, intern in res.all():
            out.append({
                "id": app.id,
                "student_id": app.student_id,
                "internship_id": intern.id,
                "title": intern.title,
                "company": intern.company,
                "role_category": intern.role_category,
                "location": intern.location,
                "is_remote": intern.is_remote,
                "status": app.status,
                "applied_at": app.applied_at,
                "deadline": app.deadline,
                "notes": app.notes,
                "updated_at": app.updated_at
            })
        return out

    async def upsert_application(
        self, 
        student_id: str, 
        internship_id: str, 
        status: str, 
        notes: Optional[str] = None
    ) -> ApplicationModel:
        stmt = select(ApplicationModel).where(
            ApplicationModel.student_id == student_id,
            ApplicationModel.internship_id == internship_id
        )
        res = await self.session.execute(stmt)
        app = res.scalar_one_or_none()
        today = date.today()
        if app:
            app.status = status
            if notes is not None:
                app.notes = notes
            if status == "applied" and not app.applied_at:
                app.applied_at = today
            app.updated_at = datetime.utcnow()
        else:
            app = ApplicationModel(
                id=f"app_{student_id}_{internship_id}",
                student_id=student_id,
                internship_id=internship_id,
                status=status,
                notes=notes or "",
                applied_at=today if status == "applied" else None,
                updated_at=datetime.utcnow()
            )
            self.session.add(app)
        await self.session.commit()
        return app

    # --- Mock Interview Operations ---
    async def get_interview_session(self, session_id: str) -> Optional[InterviewSessionModel]:
        stmt = select(InterviewSessionModel).where(InterviewSessionModel.id == session_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_session_exchanges(self, session_id: str) -> List[InterviewExchangeModel]:
        stmt = (
            select(InterviewExchangeModel)
            .where(InterviewExchangeModel.session_id == session_id)
            .order_by(InterviewExchangeModel.question_number)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Readiness Operations ---
    async def get_latest_readiness(self, student_id: str, internship_id: str) -> Optional[ReadinessRecordModel]:
        stmt = (
            select(ReadinessRecordModel)
            .where(
                ReadinessRecordModel.student_id == student_id,
                ReadinessRecordModel.target_internship_id == internship_id
            )
            .order_by(desc(ReadinessRecordModel.recorded_at))
            .limit(1)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
