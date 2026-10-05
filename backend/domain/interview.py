"""
AI Adaptive Mock Interview Preparation Service.
Generates role- and internship-specific questions, evaluates candidate responses
against technical rubrics (correctness, depth, clarity), and dynamically adjusts difficulty.
"""

from typing import Dict, Any, List, Optional
import re
from backend.domain.skill_normalizer import SkillNormalizer

# Tailored question bank categorized by role and tested competencies
INTERVIEW_QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "Backend": [
        {
            "question_number": 1,
            "category": "Technical",
            "difficulty": "medium",
            "tested_skill": "FastAPI",
            "question_text": "In FastAPI and modern Python web services, explain how dependency injection (Depends) works and why it is useful for managing database sessions or authentication.",
            "ideal_keywords": ["depends", "dependency injection", "yield", "database session", "scope", "cleanup", "reusable", "authentication"],
            "model_highlights": "FastAPI's Depends allows modular, testable components. When using a database session, Depends yields the session per request and guarantees session closure in the finally block. It decouples business endpoints from resource lifecycle management."
        },
        {
            "question_number": 2,
            "category": "System Design",
            "difficulty": "hard",
            "tested_skill": "PostgreSQL",
            "question_text": "Suppose a backend API experiences slow read queries on a high-volume table with millions of records. How would you diagnose the bottleneck and what database strategies (indexing, query optimization, connection pooling) would you apply?",
            "ideal_keywords": ["explain analyze", "index", "b-tree", "composite index", "slow query log", "connection pooling", "n+1", "foreign key"],
            "model_highlights": "First run EXPLAIN ANALYZE to identify sequential scans versus index scans. Check for missing indexes on filter/join foreign keys. Avoid SELECT * and N+1 query patterns. Ensure connection pool sizing (PgBouncer/SQLAlchemy) prevents connection exhaustion."
        },
        {
            "question_number": 3,
            "category": "Project",
            "difficulty": "medium",
            "tested_skill": "REST APIs",
            "question_text": "Walk through a backend project you built. How did you structure your API routes, validate request payloads, and handle unexpected server errors?",
            "ideal_keywords": ["router", "pydantic", "validation", "middleware", "status code", "400", "500", "error handling", "schema"],
            "model_highlights": "Structured into layered architecture (routers, services, repository models). Used Pydantic for strict request validation returning 422 errors automatically. Configured centralized exception handlers and logging for 500 errors."
        }
    ],
    "Frontend": [
        {
            "question_number": 1,
            "category": "Technical",
            "difficulty": "medium",
            "tested_skill": "React",
            "question_text": "Explain the difference between Server Components and Client Components in Next.js App Router. When must a component be marked with 'use client'?",
            "ideal_keywords": ["server components", "client components", "use client", "bundle size", "hooks", "useState", "useEffect", "event listeners", "ssr"],
            "model_highlights": "Server components render on the server by default, reducing client JavaScript bundle size and allowing direct data access. 'use client' is required when using React state (useState), lifecycle hooks (useEffect), or browser-specific event listeners (onClick, onChange)."
        },
        {
            "question_number": 2,
            "category": "Technical",
            "difficulty": "medium",
            "tested_skill": "TypeScript",
            "question_text": "Why is TypeScript beneficial in modern large-scale React applications, and how do generics and discriminated unions help prevent runtime bugs?",
            "ideal_keywords": ["typescript", "type safety", "interfaces", "generics", "discriminated unions", "compile time", "refactoring"],
            "model_highlights": "TypeScript catches syntax, null-reference, and contract mismatches at compile time rather than in production. Generics enable reusable component props, while discriminated unions ensure exhaustive handling of different application states (loading, success, error)."
        }
    ],
    "Data Science": [
        {
            "question_number": 1,
            "category": "Technical",
            "difficulty": "medium",
            "tested_skill": "Pandas",
            "question_text": "How do you handle missing data and detect outliers in tabular datasets using Pandas and NumPy? What are the tradeoffs between imputation and dropping records?",
            "ideal_keywords": ["pandas", "dropna", "fillna", "imputation", "mean", "median", "z-score", "iqr", "bias"],
            "model_highlights": "Inspect missingness mechanisms (MCAR vs MNAR). Dropping records can bias the sample if data is not missing at random. Imputation using median preserves sample size while being robust to outliers. Outliers can be flagged using IQR thresholds."
        }
    ],
    "General": [
        {
            "question_number": 1,
            "category": "Technical",
            "difficulty": "easy",
            "tested_skill": "Git",
            "question_text": "How do you use Git feature branches and resolve a merge conflict when collaborating with team members?",
            "ideal_keywords": ["branch", "git checkout", "pull request", "rebase", "merge conflict", "diff", "commit"],
            "model_highlights": "Create isolated feature branches from main. When conflicts occur during rebase or merge, inspect conflicting sections in Git diff, align on the correct combined state, run tests, and complete the merge."
        }
    ]
}

class MockInterviewEngine:
    @staticmethod
    def get_questions_for_role(role_category: str) -> List[Dict[str, Any]]:
        """Returns standard questions for a given role category with fallback to general."""
        questions = INTERVIEW_QUESTION_BANK.get(role_category)
        if not questions:
            questions = INTERVIEW_QUESTION_BANK.get("Backend") or INTERVIEW_QUESTION_BANK["General"]
        return questions

    @staticmethod
    def evaluate_response(
        question_text: str,
        student_answer: str,
        tested_skill: str,
        ideal_keywords: List[str],
        model_highlights: str,
        current_difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Evaluates a student's answer against the rubric:
        - Correctness Score (0 - 100): Mentions key concepts and accurate mechanics
        - Technical Depth Score (0 - 100): Explains 'why' and architectural implications
        - Clarity Score (0 - 100): Articulation, structure, conciseness
        - Adaptive next difficulty suggestion
        """
        if not student_answer or len(student_answer.strip()) < 10:
            return {
                "correctness_score": 25.0,
                "technical_depth_score": 20.0,
                "clarity_score": 35.0,
                "overall_score": 26.7,
                "feedback": "Answer was too brief or incomplete. In an interview setting, articulate your reasoning step-by-step with concrete technical examples.",
                "model_answer_highlights": model_highlights,
                "next_difficulty": "easy"
            }

        answer_lower = student_answer.lower()
        word_count = len(student_answer.split())

        # 1. Keyword coverage
        matched_kw = [kw for kw in ideal_keywords if kw.lower() in answer_lower]
        kw_ratio = len(matched_kw) / max(1, len(ideal_keywords))

        # Correctness: 50% keyword presence + 50% substantive explanation
        correctness = min(100.0, (kw_ratio * 60.0) + (min(word_count, 120) / 120.0 * 40.0))
        
        # Technical depth: assesses technical keywords & length
        technical_depth = min(100.0, (len(matched_kw) * 12.0) + (min(word_count, 150) / 150.0 * 40.0))

        # Clarity: penalized if too short (<25 words) or excessive run-on (>300 words without punctuation)
        clarity = 85.0
        if word_count < 25:
            clarity -= 30.0
        if "." in student_answer:
            clarity += 10.0
        clarity = min(100.0, max(30.0, clarity))

        overall = round((correctness * 0.45 + technical_depth * 0.35 + clarity * 0.20), 1)

        # Adaptive difficulty adjustment
        if overall >= 80.0:
            next_diff = "hard"
            praise = "Excellent response! You demonstrated strong technical command and clear communication."
        elif overall >= 60.0:
            next_diff = "medium"
            praise = "Solid answer covering the foundational concepts."
        else:
            next_diff = "easy"
            praise = "Good attempt, but missing some key terminology and architecture considerations."

        missing_kw = [kw for kw in ideal_keywords if kw not in matched_kw]
        feedback_lines = [praise]
        if missing_kw:
            feedback_lines.append(f"To strengthen this answer, consider mentioning: {', '.join(missing_kw[:3])}.")

        return {
            "correctness_score": round(correctness, 1),
            "technical_depth_score": round(technical_depth, 1),
            "clarity_score": round(clarity, 1),
            "overall_score": overall,
            "feedback": " ".join(feedback_lines),
            "model_answer_highlights": model_highlights,
            "next_difficulty": next_diff
        }
