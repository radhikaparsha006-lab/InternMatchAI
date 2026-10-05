-- =============================================================================
-- InternMatch AI – Supabase / PostgreSQL Schema DDL
-- Authoritative persistent relational datastore
-- =============================================================================

-- Enable UUID extension if available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Students / Users
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Student Profiles
CREATE TABLE IF NOT EXISTS student_profiles (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) UNIQUE NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    headline VARCHAR(255),
    education_degree VARCHAR(100),
    education_major VARCHAR(100),
    graduation_year INTEGER,
    gpa NUMERIC(3, 2),
    bio TEXT,
    location VARCHAR(100),
    remote_preference VARCHAR(30) DEFAULT 'flexible' CHECK (remote_preference IN ('remote_only', 'onsite_only', 'hybrid', 'flexible')),
    preferred_roles TEXT[], -- e.g. ['Backend Developer', 'Data Analyst']
    preferred_industries TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Skills Ontology
CREATE TABLE IF NOT EXISTS skills (
    id VARCHAR(64) PRIMARY KEY,
    canonical_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Languages', 'Frameworks', 'Databases', 'DevOps & Cloud', 'Data & AI', 'Tools', 'Soft Skills'
    aliases TEXT[] NOT NULL DEFAULT '{}',
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Student Skills (with provenance)
CREATE TABLE IF NOT EXISTS student_skills (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    skill_id VARCHAR(64) NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(30) DEFAULT 'intermediate' CHECK (proficiency_level IN ('beginner', 'intermediate', 'advanced')),
    provenance VARCHAR(50) DEFAULT 'user_provided' CHECK (provenance IN ('user_provided', 'resume_extracted', 'assessment_derived', 'project_derived', 'interview_verified')),
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, skill_id)
);

-- 5. Student Projects
CREATE TABLE IF NOT EXISTS student_projects (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    technologies TEXT[] NOT NULL DEFAULT '{}',
    github_url VARCHAR(255),
    live_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Internships Catalog
CREATE TABLE IF NOT EXISTS internships (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    role_category VARCHAR(100) NOT NULL, -- 'Backend', 'Frontend', 'Full Stack', 'Data Science', 'Machine Learning', 'DevOps', 'Mobile'
    location VARCHAR(100) NOT NULL,
    is_remote BOOLEAN DEFAULT FALSE,
    duration_weeks INTEGER DEFAULT 12,
    stipend VARCHAR(100),
    description TEXT NOT NULL,
    education_requirement VARCHAR(255),
    required_skills TEXT[] NOT NULL DEFAULT '{}',
    preferred_skills TEXT[] NOT NULL DEFAULT '{}',
    application_deadline DATE,
    source VARCHAR(100) DEFAULT 'curated',
    source_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Recommendation Scores & History
CREATE TABLE IF NOT EXISTS recommendation_scores (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    internship_id VARCHAR(64) NOT NULL REFERENCES internships(id) ON DELETE CASCADE,
    model_used VARCHAR(50) NOT NULL, -- 'baseline_tfidf', 'semantic_dense', 'hybrid_ranker'
    match_score NUMERIC(5, 2) NOT NULL, -- 0.00 to 100.00
    skills_score NUMERIC(5, 2) NOT NULL,
    projects_score NUMERIC(5, 2) NOT NULL,
    education_score NUMERIC(5, 2) NOT NULL,
    preferences_score NUMERIC(5, 2) NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Target-Specific Preparation Roadmaps
CREATE TABLE IF NOT EXISTS roadmaps (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    target_internship_id VARCHAR(64) NOT NULL REFERENCES internships(id) ON DELETE CASCADE,
    overall_progress NUMERIC(5, 2) DEFAULT 0.0,
    status VARCHAR(30) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, target_internship_id)
);

-- 9. Roadmap Items (Milestones & Actions)
CREATE TABLE IF NOT EXISTS roadmap_items (
    id VARCHAR(64) PRIMARY KEY,
    roadmap_id VARCHAR(64) NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    skill_id VARCHAR(64) REFERENCES skills(id),
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('critical', 'important', 'useful')),
    title VARCHAR(255) NOT NULL,
    learning_objectives TEXT NOT NULL,
    trusted_resources JSONB DEFAULT '[]'::jsonb,
    practice_project JSONB DEFAULT '{}'::jsonb,
    estimated_hours INTEGER DEFAULT 6,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Adaptive Mock Interview Sessions
CREATE TABLE IF NOT EXISTS interview_sessions (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    target_internship_id VARCHAR(64) NOT NULL REFERENCES internships(id) ON DELETE CASCADE,
    role_title VARCHAR(255) NOT NULL,
    status VARCHAR(30) DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed')),
    overall_score NUMERIC(5, 2) DEFAULT 0.0,
    feedback_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 11. Interview Exchanges (Questions & Adaptive Answers)
CREATE TABLE IF NOT EXISTS interview_exchanges (
    id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Technical', 'System Design', 'Behavioral', 'Project'
    difficulty VARCHAR(20) NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    tested_skill VARCHAR(100),
    student_answer TEXT,
    correctness_score NUMERIC(5, 2),
    technical_depth_score NUMERIC(5, 2),
    clarity_score NUMERIC(5, 2),
    feedback TEXT,
    model_answer_highlights TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Internship Readiness Index (IRI) Records
CREATE TABLE IF NOT EXISTS readiness_records (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    target_internship_id VARCHAR(64) NOT NULL REFERENCES internships(id) ON DELETE CASCADE,
    overall_iri NUMERIC(5, 2) NOT NULL, -- 0.00 to 100.00
    skill_coverage_score NUMERIC(5, 2) NOT NULL,
    project_evidence_score NUMERIC(5, 2) NOT NULL,
    roadmap_progress_score NUMERIC(5, 2) NOT NULL,
    interview_performance_score NUMERIC(5, 2) NOT NULL,
    profile_completeness_score NUMERIC(5, 2) NOT NULL,
    explanation TEXT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Application Tracker
CREATE TABLE IF NOT EXISTS applications (
    id VARCHAR(64) PRIMARY KEY,
    student_id VARCHAR(64) NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    internship_id VARCHAR(64) NOT NULL REFERENCES internships(id) ON DELETE CASCADE,
    status VARCHAR(30) DEFAULT 'saved' CHECK (status IN ('saved', 'planning_to_apply', 'applied', 'assessment', 'interview', 'offer', 'rejected', 'withdrawn')),
    applied_at DATE,
    deadline DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, internship_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_student_skills_student ON student_skills(student_id);
CREATE INDEX IF NOT EXISTS idx_student_skills_skill ON student_skills(skill_id);
CREATE INDEX IF NOT EXISTS idx_internships_role ON internships(role_category);
CREATE INDEX IF NOT EXISTS idx_internships_remote ON internships(is_remote);
CREATE INDEX IF NOT EXISTS idx_recommendation_scores_student ON recommendation_scores(student_id);
CREATE INDEX IF NOT EXISTS idx_roadmaps_student ON roadmaps(student_id);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_student ON interview_sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_readiness_records_lookup ON readiness_records(student_id, target_internship_id);
CREATE INDEX IF NOT EXISTS idx_applications_student ON applications(student_id);
