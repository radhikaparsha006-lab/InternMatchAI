"""
SQLAlchemy models corresponding to the authoritative Supabase / PostgreSQL schema.
"""

from datetime import datetime, date
from typing import List, Optional, Any
from sqlalchemy import (
    Column, String, Text, Integer, Numeric, Boolean, Date, DateTime,
    ForeignKey, CheckConstraint, UniqueConstraint, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(String(64), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("StudentProfileModel", back_populates="student", uselist=False, cascade="all, delete-orphan")
    skills = relationship("StudentSkillModel", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("StudentProjectModel", back_populates="student", cascade="all, delete-orphan")
    applications = relationship("ApplicationModel", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("RoadmapModel", back_populates="student", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSessionModel", back_populates="student", cascade="all, delete-orphan")
    readiness_records = relationship("ReadinessRecordModel", back_populates="student", cascade="all, delete-orphan")


class StudentProfileModel(Base):
    __tablename__ = "student_profiles"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    headline = Column(String(255))
    education_degree = Column(String(100))
    education_major = Column(String(100))
    graduation_year = Column(Integer)
    gpa = Column(Numeric(3, 2))
    bio = Column(Text)
    location = Column(String(100))
    remote_preference = Column(String(30), default="flexible")
    preferred_roles = Column(JSON, default=list)  # list of strings
    preferred_industries = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("StudentModel", back_populates="profile")


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(String(64), primary_key=True)
    canonical_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    aliases = Column(JSON, default=list)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class StudentSkillModel(Base):
    __tablename__ = "student_skills"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(String(64), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(String(30), default="intermediate")
    provenance = Column(String(50), default="user_provided")
    verified_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentModel", back_populates="skills")
    skill = relationship("SkillModel")

    __table_args__ = (
        UniqueConstraint("student_id", "skill_id", name="uq_student_skill"),
    )


class StudentProjectModel(Base):
    __tablename__ = "student_projects"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(JSON, default=list)
    github_url = Column(String(255))
    live_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentModel", back_populates="projects")


class InternshipModel(Base):
    __tablename__ = "internships"

    id = Column(String(64), primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    role_category = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    is_remote = Column(Boolean, default=False)
    duration_weeks = Column(Integer, default=12)
    stipend = Column(String(100))
    description = Column(Text, nullable=False)
    education_requirement = Column(String(255))
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    application_deadline = Column(Date)
    source = Column(String(100), default="curated")
    source_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class RecommendationScoreModel(Base):
    __tablename__ = "recommendation_scores"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    internship_id = Column(String(64), ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    model_used = Column(String(50), nullable=False)
    match_score = Column(Numeric(5, 2), nullable=False)
    skills_score = Column(Numeric(5, 2), nullable=False)
    projects_score = Column(Numeric(5, 2), nullable=False)
    education_score = Column(Numeric(5, 2), nullable=False)
    preferences_score = Column(Numeric(5, 2), nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RoadmapModel(Base):
    __tablename__ = "roadmaps"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    target_internship_id = Column(String(64), ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    overall_progress = Column(Numeric(5, 2), default=0.0)
    status = Column(String(30), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("StudentModel", back_populates="roadmaps")
    internship = relationship("InternshipModel")
    items = relationship("RoadmapItemModel", back_populates="roadmap", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("student_id", "target_internship_id", name="uq_roadmap_target"),
    )


class RoadmapItemModel(Base):
    __tablename__ = "roadmap_items"

    id = Column(String(64), primary_key=True)
    roadmap_id = Column(String(64), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(String(64), ForeignKey("skills.id"), nullable=True)
    skill_name = Column(String(100), nullable=True)
    priority = Column(String(20), nullable=False)  # critical, important, useful
    title = Column(String(255), nullable=False)
    learning_objectives = Column(Text, nullable=False)
    trusted_resources = Column(JSON, default=list)
    practice_project = Column(JSON, default=dict)
    estimated_hours = Column(Integer, default=6)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roadmap = relationship("RoadmapModel", back_populates="items")
    skill = relationship("SkillModel")


class InterviewSessionModel(Base):
    __tablename__ = "interview_sessions"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    target_internship_id = Column(String(64), ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    role_title = Column(String(255), nullable=False)
    status = Column(String(30), default="in_progress")
    overall_score = Column(Numeric(5, 2), default=0.0)
    feedback_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("StudentModel", back_populates="interview_sessions")
    internship = relationship("InternshipModel")
    exchanges = relationship("InterviewExchangeModel", back_populates="session", cascade="all, delete-orphan")


class InterviewExchangeModel(Base):
    __tablename__ = "interview_exchanges"

    id = Column(String(64), primary_key=True)
    session_id = Column(String(64), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    difficulty = Column(String(20), nullable=False)
    tested_skill = Column(String(100), nullable=True)
    student_answer = Column(Text, nullable=True)
    correctness_score = Column(Numeric(5, 2), nullable=True)
    technical_depth_score = Column(Numeric(5, 2), nullable=True)
    clarity_score = Column(Numeric(5, 2), nullable=True)
    feedback = Column(Text, nullable=True)
    model_answer_highlights = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSessionModel", back_populates="exchanges")


class ReadinessRecordModel(Base):
    __tablename__ = "readiness_records"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    target_internship_id = Column(String(64), ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    overall_iri = Column(Numeric(5, 2), nullable=False)
    skill_coverage_score = Column(Numeric(5, 2), nullable=False)
    project_evidence_score = Column(Numeric(5, 2), nullable=False)
    roadmap_progress_score = Column(Numeric(5, 2), nullable=False)
    interview_performance_score = Column(Numeric(5, 2), nullable=False)
    profile_completeness_score = Column(Numeric(5, 2), nullable=False)
    explanation = Column(Text, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentModel", back_populates="readiness_records")
    internship = relationship("InternshipModel")


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    internship_id = Column(String(64), ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), default="saved")
    applied_at = Column(Date, nullable=True)
    deadline = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("StudentModel", back_populates="applications")
    internship = relationship("InternshipModel")

    __table_args__ = (
        UniqueConstraint("student_id", "internship_id", name="uq_student_internship_app"),
    )
