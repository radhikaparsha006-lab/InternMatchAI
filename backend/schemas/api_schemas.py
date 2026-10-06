"""
Pydantic V2 request and response schemas for all API domains.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field

# --- Profile & Skills ---
class SkillItem(BaseModel):
    id: Optional[str] = None
    canonical_name: str
    category: Optional[str] = "General"
    proficiency_level: str = "intermediate"
    provenance: str = "user_provided"

class ProjectItem(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    technologies: List[str] = []
    github_url: Optional[str] = ""
    live_url: Optional[str] = ""

class ProfileData(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = ""
    education_degree: Optional[str] = ""
    education_major: Optional[str] = ""
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None
    bio: Optional[str] = ""
    location: Optional[str] = ""
    remote_preference: Optional[str] = "flexible"
    preferred_roles: List[str] = []
    preferred_industries: List[str] = []

class StudentResponse(BaseModel):
    id: str
    email: str
    full_name: str
    profile: Optional[ProfileData] = None
    skills: List[SkillItem] = []
    projects: List[ProjectItem] = []

class AddSkillRequest(BaseModel):
    skill_name: str
    proficiency_level: Optional[str] = "intermediate"

class ResumeParseRequest(BaseModel):
    resume_text: str

class ResumeParseResponse(BaseModel):
    full_name: str
    headline: str
    education_degree: str
    education_major: str
    graduation_year: Optional[int]
    gpa: Optional[float]
    skills: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    bio: str

# --- Internships ---
class InternshipResponse(BaseModel):
    id: str
    title: str
    company: str
    role_category: str
    location: str
    is_remote: bool
    duration_weeks: int
    stipend: Optional[str] = ""
    description: str
    education_requirement: Optional[str] = ""
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    application_deadline: Optional[date] = None
    source: Optional[str] = "curated"
    source_url: Optional[str] = ""

# --- Recommendations ---
class ScoreBreakdown(BaseModel):
    skills_score: float
    projects_score: float
    education_score: float
    preferences_score: float
    semantic_score: Optional[float] = None

class RecommendationItem(BaseModel):
    internship_id: str
    match_score: float
    breakdown: ScoreBreakdown
    explanation: str
    matched_required_skills: List[str] = []
    matched_preferred_skills: List[str] = []
    missing_required_skills: List[str] = []
    internship: InternshipResponse

class RecommendationListResponse(BaseModel):
    model_used: str
    total_recommendations: int
    items: List[RecommendationItem]

# --- Skill Gap ---
class GapItem(BaseModel):
    skill_name: str
    category: str
    priority: str
    reason: str

class SkillGapResponse(BaseModel):
    target_internship_id: str
    internship_title: str
    company: str
    role_category: str
    coverage_percentage: float
    severity: str
    matched_skills: Dict[str, List[str]]
    gaps: Dict[str, List[GapItem]]

# --- Roadmap ---
class TrustedResource(BaseModel):
    title: str
    url: str
    platform: str
    type: str
    estimated_hours: str

class RoadmapItemData(BaseModel):
    id: str
    skill_name: str
    priority: str
    title: str
    learning_objectives: str
    trusted_resources: List[TrustedResource] = []
    practice_exercise: str
    estimated_hours: int
    is_completed: bool

class RecommendedProject(BaseModel):
    title: str
    description: str
    technologies: List[str]
    deliverables: List[str]

class RoadmapResponse(BaseModel):
    student_id: str
    target_internship_id: str
    internship_title: str
    company: str
    role_category: str
    total_estimated_hours: int
    overall_progress: float
    items: List[RoadmapItemData]
    recommended_project: Optional[RecommendedProject] = None

class ToggleRoadmapItemRequest(BaseModel):
    is_completed: bool

# --- Interview ---
class StartInterviewRequest(BaseModel):
    student_id: str
    target_internship_id: str

class InterviewQuestionData(BaseModel):
    question_number: int
    question_text: str
    category: str
    difficulty: str
    tested_skill: str

class StartInterviewResponse(BaseModel):
    session_id: str
    target_internship_id: str
    role_title: str
    first_question: InterviewQuestionData

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_number: int
    student_answer: str

class SubmitAnswerResponse(BaseModel):
    question_number: int
    correctness_score: float
    technical_depth_score: float
    clarity_score: float
    overall_score: float
    feedback: str
    model_answer_highlights: str
    next_question: Optional[InterviewQuestionData] = None
    session_complete: bool = False
    average_session_score: Optional[float] = None

# --- Readiness ---
class ReadinessComponents(BaseModel):
    skill_coverage: float
    project_evidence: float
    roadmap_progress: float
    interview_performance: float
    profile_completeness: float

class ReadinessResponse(BaseModel):
    target_internship_id: str
    overall_iri: float
    components: ReadinessComponents
    matched_required_skills: List[str]
    missing_required_skills: List[str]
    explanation: str

# --- Applications ---
class ApplicationItem(BaseModel):
    id: str
    student_id: str
    internship_id: str
    title: str
    company: str
    role_category: str
    location: str
    is_remote: bool
    status: str
    applied_at: Optional[date] = None
    deadline: Optional[date] = None
    notes: Optional[str] = ""
    updated_at: Optional[datetime] = None

class UpsertApplicationRequest(BaseModel):
    internship_id: str
    status: str
    notes: Optional[str] = ""
