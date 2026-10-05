"""
Adaptive Mock Interview Router.
Conducts role-specific interview sessions, evaluates responses using multi-dimensional rubrics,
adapts difficulty, and verifies student skills upon strong performance.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from backend.database.connection import get_db
from backend.database.repository import DataRepository
from backend.database.models import InterviewSessionModel, InterviewExchangeModel
from backend.schemas.api_schemas import (
    StartInterviewRequest, StartInterviewResponse, InterviewQuestionData,
    SubmitAnswerRequest, SubmitAnswerResponse
)
from backend.domain.interview import MockInterviewEngine, INTERVIEW_QUESTION_BANK
from backend.domain.closed_loop import ClosedLoopCoordinator

router = APIRouter(prefix="", tags=["Mock Interview"])

@router.post("/interview/start", response_model=StartInterviewResponse)
async def start_interview(req: StartInterviewRequest, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    student = await repo.get_student(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    internship = await repo.get_internship_by_id(req.target_internship_id)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    session_model = InterviewSessionModel(
        id=session_id,
        student_id=req.student_id,
        target_internship_id=req.target_internship_id,
        role_title=internship.title,
        status="in_progress",
        overall_score=0.0
    )
    db.add(session_model)

    questions = MockInterviewEngine.get_questions_for_role(internship.role_category)
    for q in questions:
        exchange_model = InterviewExchangeModel(
            id=f"{session_id}_q{q['question_number']}",
            session_id=session_id,
            question_number=q["question_number"],
            question_text=q["question_text"],
            category=q["category"],
            difficulty=q["difficulty"],
            tested_skill=q["tested_skill"]
        )
        db.add(exchange_model)

    await db.commit()

    first_q = questions[0]
    return StartInterviewResponse(
        session_id=session_id,
        target_internship_id=req.target_internship_id,
        role_title=internship.title,
        first_question=InterviewQuestionData(
            question_number=first_q["question_number"],
            question_text=first_q["question_text"],
            category=first_q["category"],
            difficulty=first_q["difficulty"],
            tested_skill=first_q["tested_skill"]
        )
    )

@router.post("/interview/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(req: SubmitAnswerRequest, db: AsyncSession = Depends(get_db)):
    repo = DataRepository(db)
    session = await repo.get_interview_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    exchanges = await repo.get_session_exchanges(req.session_id)
    current_exchange = next((e for e in exchanges if e.question_number == req.question_number), None)
    if not current_exchange:
        raise HTTPException(status_code=404, detail="Question not found in session")

    # Retrieve ideal keywords & highlights for this question
    internship = await repo.get_internship_by_id(session.target_internship_id)
    role_cat = internship.role_category if internship else "Backend"
    q_bank = MockInterviewEngine.get_questions_for_role(role_cat)
    matched_q = next((q for q in q_bank if q["question_number"] == req.question_number), q_bank[0])

    evaluation = MockInterviewEngine.evaluate_response(
        question_text=current_exchange.question_text,
        student_answer=req.student_answer,
        tested_skill=current_exchange.tested_skill or "",
        ideal_keywords=matched_q.get("ideal_keywords", []),
        model_highlights=matched_q.get("model_highlights", ""),
        current_difficulty=current_exchange.difficulty
    )

    current_exchange.student_answer = req.student_answer
    current_exchange.correctness_score = evaluation["correctness_score"]
    current_exchange.technical_depth_score = evaluation["technical_depth_score"]
    current_exchange.clarity_score = evaluation["clarity_score"]
    current_exchange.feedback = evaluation["feedback"]
    current_exchange.model_answer_highlights = evaluation["model_answer_highlights"]

    # Closed-loop skill verification if high score
    coordinator = ClosedLoopCoordinator(repo)
    await coordinator.handle_interview_performance_verified(
        student_id=session.student_id,
        target_internship_id=session.target_internship_id,
        tested_skill=current_exchange.tested_skill,
        score=evaluation["overall_score"]
    )

    # Next question or finish
    next_q_num = req.question_number + 1
    next_exchange = next((e for e in exchanges if e.question_number == next_q_num), None)

    next_q_data = None
    session_complete = False
    avg_score = None

    if next_exchange:
        # Adapt difficulty
        next_exchange.difficulty = evaluation["next_difficulty"]
        next_q_data = InterviewQuestionData(
            question_number=next_exchange.question_number,
            question_text=next_exchange.question_text,
            category=next_exchange.category,
            difficulty=next_exchange.difficulty,
            tested_skill=next_exchange.tested_skill or ""
        )
    else:
        session_complete = True
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        # Compute session average
        answered_scores = [
            float(e.correctness_score or 0.0) * 0.45 +
            float(e.technical_depth_score or 0.0) * 0.35 +
            float(e.clarity_score or 0.0) * 0.20
            for e in exchanges if e.correctness_score is not None
        ]
        if answered_scores:
            avg_score = round(sum(answered_scores) / len(answered_scores), 1)
            session.overall_score = avg_score
            session.feedback_summary = f"Completed mock interview with average readiness score of {avg_score}/100."

    await db.commit()

    return SubmitAnswerResponse(
        question_number=req.question_number,
        correctness_score=evaluation["correctness_score"],
        technical_depth_score=evaluation["technical_depth_score"],
        clarity_score=evaluation["clarity_score"],
        overall_score=evaluation["overall_score"],
        feedback=evaluation["feedback"],
        model_answer_highlights=evaluation["model_answer_highlights"],
        next_question=next_q_data,
        session_complete=session_complete,
        average_session_score=avg_score
    )
